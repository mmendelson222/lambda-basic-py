from boto import ec2
region = "us-east-1" #raw_input ("which region?")
conn = ec2.connect_to_region(region)

# reservation list:
reservations = conn.get_all_instances()

# security group list
sg_array = []

# dictionary with instances and security groups:

ins_sg = {}

# loop through instances (reservations):
for i in reservations:

# check how many SGs are attached to instance
    group_nums = len(i.instances[0].groups)
    print "######################\n"
    print "InstanceID: %s\n" % i.instances[0]
    print "Number of SGs attached: %s\n" % group_nums
# go through each SG
    for z in range(group_nums):
# find id for each SG
        group_id = i.instances[0].groups[z].id
        sg_name = conn.get_all_security_groups(group_ids=group_id)[0]
# describe rules for each SG
        sec_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules
# calculate number of rules
        rule_nums = len(sec_rules)
# print SG name
        print "%s\n" % sg_name
# print SG Ingress rules
        print "Ingress Rules:\n\n"
        for g in range(rule_nums):
            print "Port/protocol: %s" % conn.get_all_security_groups(group_ids=group_id)[0].rules[g]
            print "Source: %s" % conn.get_all_security_groups(group_ids=group_id)[0].rules[g].grants
        print "\n\n"
# number of Egress rules
        egress_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules_egress
        number_of_egress = len(egress_rules)
        print "Egress Rules:\n\n"
        for k in range(number_of_egress):
            print "Port/protocol: %s" % conn.get_all_security_groups(group_ids=group_id)[0].rules_egress[k]
            print "Destination: %s" % conn.get_all_security_groups(group_ids=group_id)[0].rules_egress[k].grants

        print "\n\n"