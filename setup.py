import csv

from configurations import *


def get_points(course,grade,none_credit = False):
    try:
        _grade = GRADING[grade]
    except:
        raise ValueError(f"{grade} is not valid grading.")
    try:
        _credit =  course_weight[course]["WEIGHT"] if not (none_credit and course_weight[course]["isNoneCredit"]) else 0
    except:
        raise ValueError(f"{course} is not a valid course. check the courses.csv file.")
    return _grade * _credit, _credit

def get_wgpa():
    wgpa = 0
    _v = 0
    for k, i in year_dict.items():
        if k in VALID_YEARS:
            year_gpa = i.get("CGPA",0)
            ratio = WGPA_DICT[k]
            _v += ratio
            wgpa += year_gpa * ratio

    if _v == 1:
        return wgpa
    else:
        raise ValueError(f"total wgpa ratio must be 1. now it is {_v}")

def print_details():
    for k, i in year_dict.items():
        if k in VALID_YEARS:
            print(f"################################ YEAR 0{k[1]} ################################")
            print("### Total credit: {:.2f}\t### Total points: {:.2f}\t### Year CGPA: {:.2f}".format(i['TOTAL_CREDIT'],i['TOTAL_POINT'],i['CGPA']))
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
            c_len = len(i["COURSES"])
            col = 3
            row = (c_len// col ) +1
            # row = row + 1 if c_len == col * row else row
            c_len_count = 0
            for ind in range(row):
                _string = ""
                # try:
                for jnd in range(col):
                    try:
                        c = i["COURSES"][c_len_count]
                    except:
                        break
                    _g = c['GRADE'] if len(c['GRADE']) ==2 else c['GRADE'] + " "
                    _string += "{}. {}\t| {}\t| {:.1f}\t\t|*|\t".format(str(c_len_count+1).zfill(2),c['COURSE'],_g,c['CREDIT'])
                    c_len_count += 1
                print(_string.rstrip("|*|\t"))
                # except IndexError:
                #     break

            print("_________________________________________________________")




            # for c in i["COURSES"]:
            #     print(f"{c['COURSE']}\t| {c['GRADE']}\t| {c['CREDIT']}")




year_dict = {"01Y": {"COURSES": []},
             "02Y": {"COURSES": []},
             "03Y": {"COURSES": []},
             "04Y": {"COURSES": []},
             }
course_weight = {}
with open('courses.csv') as result_file:
    csv_reader = csv.reader(result_file, delimiter=',')
    for row in csv_reader:
        isNoneCredit = True if row[2].__contains__("None") else False
        try:
            course_weight[row[0]] = { "WEIGHT": int(row[1]), "isNoneCredit" : isNoneCredit}
        except:
            pass



with open('results.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    _year = 0
    for row in csv_reader:
        if row[0].startswith("Year "):
            if _year != int(row[0][5]):
                course = []

            _year = int(row[0][5])
        else:
            course.append({"COURSE": row[0],
                           "GRADE": row[2],
                           "CREDIT": None
                           })
            year_dict[f"0{_year}Y"]["COURSES"] = course

        line_count += 1


cumulative_grade_points = 0
cumulative_credit = 0

for k,i in year_dict.items():
    cgpa_point = 0
    total_credit = 0
    if k in VALID_YEARS:
        for __course in i["COURSES"]:
            _point, _credit = get_points(__course["COURSE"], __course["GRADE"],none_credit=True)
            cgpa_point += _point
            total_credit += _credit
            __course["CREDIT"] = _credit

        i["TOTAL_POINT"]=cgpa_point
        i["TOTAL_CREDIT"]=total_credit
        i["CGPA"] = cgpa_point / total_credit


        cumulative_grade_points += cgpa_point
        cumulative_credit += total_credit


WGPA = get_wgpa()
TOTAL_CGPA = cumulative_grade_points / cumulative_credit

print("TOTAL CGPA: {:.2f}\t| Weighted GPA: {:.2f}".format(TOTAL_CGPA,WGPA))
print("##########################################")
print_details()







#     if line_count == 0:
#         print(f'Column names are {", ".join(row)}')
#         line_count += 1
#     else:
#         print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#         line_count += 1
# print(f'Processed {line_count} lines.')
