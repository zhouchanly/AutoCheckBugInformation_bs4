import time
import traceback
from businesslogic import BusinessLogic
from filepath import Filepath
from readfromexcel import ReadExcel
from review import Review
from singlereport import Singlereport
from writeintoexcel import WriteExcel

if __name__=="__main__":
    path = Filepath()
    jiradict = path.projectlist_file()
    s = Singlereport()
    writeexcel = WriteExcel()
    review = Review()

    try:
        #jira_value 为项目的jira键值，如GGXB,KR
        for jira_value in jiradict:
            # 项目名称，如咕咕机，咕咕机海外版，coolpro G2
            jira_sheetname = jiradict[jira_value]
            print(jira_sheetname)
            read_excel = ReadExcel(jira_value, jira_sheetname)
            # excel中是否有项目检查记录，没有会先新建表格
            project_exist = read_excel.project_if_exist()

            ###判断是否需要复查###
            # 通过配置文件加进来。excel中有项目检查记录，复查
            need_review = 1
            if need_review:
                #projectlist中要检查的项目已经在汇总表格中有sheet页面
                if project_exist:
                    review_jiraid_position = review.get_review_url(jira_value)  # 项目存在，复查
                    if review_jiraid_position:
                        for review_jiraid in review_jiraid_position.keys():
                            bug_infor_review = BusinessLogic(review_jiraid)
                            bug_infor_review_result = bug_infor_review.check_item()
                            print(bug_infor_review_result)
                            row = review_jiraid_position.get(review_jiraid)[0]
                            cols = review_jiraid_position.get(review_jiraid)[1]
                            #单份报告
                            s_rep = path.single_report()
                            s_rep_path = s_rep[0]
                            s_rep_sheetname = s_rep[1]
                            if bug_infor_review_result[0] != '':
                                review.review_bug_nonconformity(jira_value, row, cols, '不符合',
                                                                bug_infor_review_result[0],
                                                                bug_infor_review_result[1], time.strftime("%Y/%m/%d"))
                                s.create_write_report(s_rep_path, s_rep_sheetname, review_jiraid,
                                                      bug_infor_review_result[0], bug_infor_review_result[1])
                            else:
                                review.review_bug_nonconformity(jira_value, row, cols, '符合', bug_infor_review_result[0],
                                                                bug_infor_review_result[1], time.strftime("%Y/%m/%d"))
                                # s.create_write_report(s_rep_path, s_rep_sheetname, review_jiraid,bug_infor_review_result[0], bug_infor_review_result[1])
                                # todo 符合就不用写在单次的报告里面了才是，等实际复查的时候测试一下
                        print("复查完毕")

                # projectlist中要检查的项目在汇总表格无sheet页面。说明新项目，没有检查过。不用复查
                else:
                    print("新项目，不复查")
                    pass
            else:
                print("不进行复查")
                pass

            ###检查新的问题提交规范###
            # 问题是否存在的标志位
            exist_flag = []
            #从汇总的表格中读取上次检查记录的最后一个jiraid
            latest_check_id = read_excel.latest_id()
            print('最后一次检查的序号为 %s' % latest_check_id)
            for id in range(latest_check_id, 9999):
                jiraid = str(jira_value + '-' + str(id))  # 比如 GGXB-12 KR-435
                print("目前正在检查 %s"%jiraid)
                buginformation = BusinessLogic(jiraid)

                ###判断问题是否存在###
                flag = buginformation.issue_exist()
                # 问题存在
                if flag:
                    exist_flag = []
                    infor_check = buginformation.check_item()
                    print(infor_check)
                    if infor_check[0] != '':
                        writeexcel.write_non_conformity(read_excel.latest_nrows(), jira_value, jiraid,
                                                    infor_check[0], infor_check[1],
                                                    time.strftime("%Y/%m/%d"))
                        read_excel.latest_nrows() + 1
                        #单份报告
                        s_rep = path.single_report()
                        s_rep_path = s_rep[0]
                        s_rep_sheetname = s_rep[1]
                        s.create_write_report(s_rep_path, s_rep_sheetname, jiraid, infor_check[0],
                                              infor_check[1])
                    else:
                        print("bug内容无不规范项")
                        writeexcel.write_lates_id(read_excel.latest_nrows(), jira_value, jiraid)
                    #TODO 添加写入表格的
                # 问题不存在，需要连续判断3个，如果接下来3个都不存在就认为当前问题是最新的一个
                else:
                    exist_flag.append(id)
                    # print(exist_flag)
                    if len(exist_flag) == 3 and (exist_flag[2] - exist_flag[0] == 2):
                        print('问题真的不存在')  # id应该从一开始的计算，或者不写入表格内。然后进入下一个项目检查
                        exist_flag = []
                        break
        backpath = path.backup_file()
        summarypath = path.summary_report()
        path.backup_summary(summarypath, backpath)  # 备份汇总报告
        traceback.print_exc()  # 打印异常
    except BaseException:
        backpath = path.backup_file()
        summarypath = path.summary_report()
        path.backup_summary(summarypath, backpath)  # 备份汇总报告
        traceback.print_exc()  # 打印异常





