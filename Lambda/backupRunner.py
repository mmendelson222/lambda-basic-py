##################################################################################
# Please don't modify anything under this line unless you know what you are doing:
##################################################################################
from __future__ import print_function
import boto3
import botocore
from boto3.session import Session
import datetime
import os
import time
import logging
import sys, getopt
import croniter


#--------------------------------------------------------------------------------
# Function to compile the list of instances based on the matching tags and cron schedule
#--------------------------------------------------------------------------------

def filterInstances(instanceList,tag,region,lgr, Instcsv_file):
    backup_list = []

    
    for inst in instanceList:
        name = [t['Value'] for t in inst.tags if t['Key'] == 'Name']
        #owner = [t['Value'] for t in inst.tags if t['Key'] == 'Owner'] 
        #owner = inst.tags['Owner'] if 'Owner' in inst.tags else "OwnerTagMissing"
        state = inst.state['Name']
        tvalue = [t["Value"] for t in inst.tags if t["Key"] == tag]
        tags = [x.strip() for x in tvalue[0].split(";")]

        if len(tags) == 3:
            backup_sched = tags[0] if tags[0] else None
            override = tags[2] if tags[2] else None

            if backup_sched == None: 
                    lgr.info( "NO backup schedule for %s,%s,%s" % (inst.id, name[0], state))                
            
            if backup_sched != None and time_to_action(start_sched, stop_sched, state, inst.id, lgr, Instcsv_file):
                    stop_list.append(inst.id)
                    lgr.info( "%s,%s,%s,%s,%s,New State:Stopped" % (inst.id, name[0], stop_sched, start_sched, state))
                    Instcsv_file.write("%s,%s,%s,Stopped,%s,%s,%s,%s,%s\n" % (name[0],
                    inst.id,state,inst.private_ip_address,
                    inst.vpc_id,inst.subnet_id,override,region))

            #if override != "Yes":
                
            #elif override == "Yes":
            #    lgr.info("Instances that have override flag, %s, %s" % (name[0],inst.id))
            #    Instcsv_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (name,
            #        inst.id,state,state,inst.private_ip_address,
            #        inst.vpc_id,inst.subnet_id,override,region))
            #    continue
        else:
            lgr.info("Instances that are not properly tagged, %s, %s" % (name[0],inst.id))
            continue

    return backup_list

#--------------------------------------------------------------------------------
# Function to determine if an instance is scheduled to stop or start
#--------------------------------------------------------------------------------
def time_to_action(start_sched, stop_sched, state, id1, lgr, Instcsv_file):
    
    now = datetime.datetime.now()
    try:
        if start_sched != None:
            startcron = croniter.croniter(start_sched, now)
            nextstart = startcron.get_next(datetime.datetime)
            prevstart = startcron.get_prev(datetime.datetime)
            lgr.debug( "%s, Now: %s, NextStart: %s, PrevStart: %s " % (id1, now, nextstart, prevstart))
        if stop_sched != None:
            stopcron = croniter.croniter(stop_sched, now)
            nextstop = stopcron.get_next(datetime.datetime)
            prevstop = stopcron.get_prev(datetime.datetime)
            lgr.debug( "%s, Now: %s, NextStop: %s and PrevStop: %s " % (id1, now, nextstop, prevstop))  
        if (state =='stopped'):
            if (stop_sched != None):
                tstop = (prevstart <= prevstop <= now)
                ret = (prevstart<= now <=nextstop) and (tstop != True)  
            else:
                ret = False
        elif (state =='running'):
            if (start_sched != None):
                tstart = (prevstop <= prevstart <= now)
                ret = (prevstop <= now <= nextstart) and (tstart != True)
            else:
                ret = False
        else:
            ret = False

    except Exception, e:
        lgr.info( "Caught Exception: %s" % (e))
        lgr.info( "Instance-id %s state will remain the same [%s]" % (id1, state))
        ret = False
    return ret

def handler(event, context):
    
    subject = 'Lambda: Instance Scheduler Summary'
    #--------------------------------------------------------------------------------
    lgr = logging.getLogger('STOP-START-LOG')
    #logfilename = 'EC2-STOP-START'+str(time.strftime("_%Y%m%d_%H%M"))+".log"
    logfilename = 'EC2-STOP-START.log'
    lgr.setLevel(logging.INFO)
    fh = logging.FileHandler(os.path.join("./"+logfilename))
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(frmt)
    lgr.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(frmt)
    lgr.addHandler(sh)

    #--------------------------------------------------------------------------------
    # Initializing the csv file at /tmp/ and other variables for email
    #--------------------------------------------------------------------------------

    file_location = ('./Instances.csv')
    Instcsv_file = open(file_location,'w+')
    Instcsv_file.write("Name,Instance Id,Current State,State Change,Private IP,VPC,SubnetId,OverrideFlag,Region,\n")


    # Connect to EC2, and iterate through all EC2 regions to identify the qualified instances.
    #try:
    session = boto3.Session()
    ec2client = session.client('ec2')

    regions = []
    tag = "smx-backup"

    Regions = ec2client.describe_regions()
    for i in Regions['Regions']:
        regions.append(i['RegionName'])

    for region in regions:
        conn = session.resource('ec2', region_name = region)
        allInstances = conn.instances.filter(Filters=[{'Name': 'tag-key', 'Values':[tag]}])
        
        if allInstances > 0:
            backup_list = filterInstances(allInstances,tag,region,lgr, Instcsv_file)
            # Print summary of filtered instances
            lgr.info( "Number of instances being processed in %s to back up: %d" % (region, len(backup_list)))

            # Execute BACKUP code
            #if len(start_list) > 0:
            #    lgr.info("Following EC2 instances will be started : %s\n " %(backup_list))
            #    start_response = ec2client.start_instances(InstanceIds = backup_list)

        else:
            continue

    Instcsv_file.close()

    return 

if __name__ == "__main__":
    handler({'Organization': 'NPO1'}, "Dummy Data")