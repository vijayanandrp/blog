import re

file_path = '/home/vijay/Documents/code/case_class.scala'

fp =  open(file_path).readlines()

fp = " ".join(fp)

group = re.findall('case class(.*?)\(', fp)

# print(group, len(group), len(set(group)))
group = list(set(group))
group.sort()
group = [_.strip() for _ in group if _.strip()]
case_dict = dict()
# print(fp)
for case in group:
    case = case.strip()
    # print(case, re.findall('case class {0} \((.*?)\)'.format(case), fp, re.DOTALL))
    if case not in case_dict.keys():
        case_dict[case] = ", ".join(re.findall('case class {0} \((.*?)\)'.format(case), fp, re.DOTALL)).replace('\n', '')
    else:
        case_dict[case] += ", ".join(re.findall('case class {0} \((.*?)\)'.format(case), fp, re.DOTALL)).replace('\n', '')

# print(case_dict.keys())
fw = open("/home/vijay/Documents/code/parse_case_class.scala", "w")
for case in group:
    if case not in case_dict.keys():
        print("Case ", case,  " is missing.")
        continue

    fields = case_dict[case]
    fields  = [field.replace("type :", "typed :").strip()  for field in fields.split(",") if field.strip()]
    fields = list(set(fields))
    fields.sort()
    value = "case class {0} ( {1} ) \n".format(case, ", ".join(fields))
    fw.write(value)


fw.close()
