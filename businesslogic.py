import re

from elementanalysis import Elementanalysis
from filepath import Filepath


class BusinessLogic(object):
    def __init__(self,jiraid):
        self.jiraid = jiraid
        url = 'http://jira.intretech.com:8080/browse/' + jiraid
        e = Elementanalysis(url)   #GGXB-4517  4517
        # 问题详情-类型
        self.type_val = e.type_val()
        # 问题详情-状态
        self.bug_status = e.bug_status()
        # 问题详情-影响版本
        self.versions_val = e.versions_val()
        #问题详情-修复版本
        self.fixfor_val = e.fixfor_val()
        # 问题详情-解决结果
        self.bug_status_type = e.bug_status_type()
        # 问题详情-模块
        self.components = e.components()
        # 问题详情-发生概率
        self.probability_of_occurrence = e.probability_of_occurrence()
        # 问题详情-前提条件
        self.premise_condition = e.premise_condition()
        self.steps = e.steps()
        # 问题详情-实际结果
        self.actual_results = e.actual_results()
        # 问题详情-预期结果
        self.expected_results = e.expected_results()
        # 问题详情-影响范围
        self.scope_of_influence = e.scope_of_influence()
        # 问题详情-是否提交代码
        self.submit_code = e.submit_code()
        # 问题详情-原因分析
        self.cause_analysis = e.cause_analysis()
        # 问题详情-解决措施
        self.solution = e.solution()
        # 提取描述内容
        self.description = e.description()
        # 附件有无判断
        self.attachment = e.attachment()
        #提取 活动中所有的项对应的链接
        self.activity_link = e.activity_link()
        # 提取 活动-备注中的内容
        self.comment = e.comment()
        # 提取 活动-所有中的“创建问题”，这部分是需要重新获取连接解析的
        # self.activities_all = e.activities_all()
        # 经办人
        self.assignee = e.assignee()
        #报告人
        self.reporter = e.reporter()
        # 创建时间
        self.creat_date = e.creat_date()
        # 解决时间
        self.resolved_date = e.resolved_date()
        # 问题不存在,其实是提取bug的标题（网页显示的标题）
        self.issuecontent = e.issuecontent()
        # 提取父链接id
        self.parent_issue = e.parent_issue()
        # 判断父链接是否为buglist  #TODO 这里有问题，父级连接时要重新获取才能得到父问题类型，不是这里给的
        # self.parent_type_val = e.parent_type_check()
        # 提取 问题-主题
        self.summary = e.summary()

    #问题是否存在  ---完成
    def issue_exist(self):
        # print(self.issuecontent)
        if self.issuecontent == '问题不存在':
            return False
        else:
            return True


    #判断报告人是否是测试人员 ---完成
    def reporter_check(self):
        testerlist = Filepath()
        reporter_dict = testerlist.reporter_file()
        if self.reporter in reporter_dict.keys():
            print("测试者：", reporter_dict[self.reporter])
            return reporter_dict[self.reporter]
        else:
            print("非测试人员提交")
            return False

    #判断经办人是否是开发人员 ---完成
    def assignee_check(self):
        assigneelist = Filepath()
        assignee_dict = assigneelist.assignee_file()
        if self.assignee in assignee_dict.keys():
            print("开发者：", assignee_dict[self.assignee])
            return assignee_dict[self.assignee]
        else:
            print("非开发工程师提交")
            return False

    #判断“问题详情-类型”的内容；“子任务开展”的父级问题类型判断  ---完成
    def type_check(self):
        #单条问题
        if self.type_val == '问题点':
            return True
        #有父级
        elif self.type_val  == '子任务开展':
            print("父级jiraid号：%s" %self.parent_issue)
            url = 'http://jira.intretech.com:8080/browse/'+ str(self.parent_issue)
            parent_analysis = Elementanalysis(url)
            parent_type_val = parent_analysis.type_val()
            parent_issuecontent = parent_analysis.issuecontent()
            if parent_type_val == '问题点':
                return True
            else:
                match_str = "Buglist|buglist|问题集"

                match = re.findall(match_str, str(parent_issuecontent))
                if len(match) != 0:
                    return True
                else:
                    return False
        else:
            #单条问题不是问题点
            return False

    def buglist_title_check(self):
        match_str = "Buglist|buglist|问题集"
        match = re.findall(match_str, str(self.summary))
        # print(str(self.summary))
        # print(match)
        if len(match) != 0:
            #是buglist问题集合
            # print("是buglist问题集合")
            return False
        else:
            #不是buglist问题集合
            # print("不是buglist问题集合")
            return True


    #bug描述信息判断   要判断两个地方：“问题详情”部分，“描述”部分 --完成
    def description_check(self):
        s=''
        match_str = "概率"
        match_result = re.findall(match_str, str(self.description))
        match_str1 = "前置|前提|预置"
        match_result1 = re.findall(match_str1, str(self.description))
        match_str2 = "操作步骤"
        match_result2 = re.findall(match_str2, str(self.description))
        match_str3 = "预期结果|期望结果|预期输出"
        match_result3 = re.findall(match_str3, str(self.description))
        match_str4 = "实际结果|实际输出"
        match_result4 = re.findall(match_str4, str(self.description))
        #问题详情的bug描述：
        describe1 = self.probability_of_occurrence== False and self.premise_condition== False  and self.steps== False  and self.actual_results== False  and self.expected_results== False
        #描述里的bug描述：
        describe2 = len(match_result1) == 0 and len(match_result2) == 0 and len(match_result3) == 0 and len(match_result4) == 0
        if describe1 and describe2 :
            if self.attachment:
                s += "bug描述没有写;"
            else:
                s += "bug描述没有写也没有附件说明;"
        else:
            if self.probability_of_occurrence == False and len(match_result) == 0:
                s += "发生概率没有写;"
            if self.premise_condition == False and len(match_result1) == 0:
                s += "前提条件没有写;"
            if self.steps == False and len(match_result2) == 0:
                s += "操作步骤没有写;"
            if self.actual_results == False and len(match_result4) == 0:
                s += "实际结果没有写;"
            if self.expected_results == False and len(match_result3) == 0:
                s += "预期结果没有写;"
        return s


    # 解决措施 填写规范判断---完成
    def solution_check(self):
        s = ''
        # print(self.solution)
        #先判断此问题是否和其他问题重复，如果重复有的开发会直接放链接过来，如：HTSF-1004，HTSF-1087
        match_xiangtong = "[A-Z]*-[0-9]*"
        match__xiangtong_result = re.findall(match_xiangtong, str(self.solution))
        # print(match__xiangtong_result)
        if len(match__xiangtong_result) == 0:
            if self.submit_code and self.cause_analysis and self.solution: #self.scope_of_influence 影响范围不检查
                pass
            else:
                if self.solution == False:
                    s += '“解决措施”没写；'
                else:

                    match_str1 = "问题原因|原因|由于"
                    match_result1 = re.findall(match_str1, str(self.solution))
                    match_str2 = "解决措施|解决办法|措施"
                    match_result2 = re.findall(match_str2, str(self.solution))
                    # match_str3 = "影响范围"
                    # match_result3 = re.findall(match_str3, str(self.solution))
                    match_str4 = "提交"
                    match_result4 = re.findall(match_str4, str(self.solution))
                    # print(match_result1,match_result2,match_result3,match_result4)
                    if len(match_result1) == 0 and self.cause_analysis == False:
                        s += '“原因分析”没写；'
                    if len(match_result2) == 0 and self.cause_analysis == False and self.scope_of_influence == False and self.submit_code == False:
                        s += '“解决措施”填写不规范；'
                    #影响范围不检查
                    # if len(match_result3) == 0 and self.scope_of_influence == False:
                    #     s += '“影响范围”没写；'
                    if len(match_result4) == 0 and self.submit_code == False:
                        s += '“是否提交代码”没写；'
            return s
        else:
            #问题重复，开发有备注见哪个问题
            pass
            return s




    #修复版本填写判断  因为有的工程师是把“修复版本”写在“问题详情-解决措施”里了
    def fix_version_check(self):
        s = ''
        if self.fixfor_val == '无':
            match_str = "修复版本"
            match_result = re.findall(match_str, str(self.solution))
            if len(match_result) == 0:
                print('问题详情-解决措施 里没有“修复版本”')
                s += '“修复版本”没写；'
            else:
                #修复版本有写，写在'问题详情-解决措施“里面
                pass
        else:
            #修复版本有写，写在“修复版本里面
            pass
        return s



    #影响版本是否填写
    def affect_version_check(self):
        s = ''
        if self.versions_val == '无':
            s += '“影响版本”没写；'
        else:
            #影响版本有写
            pass
        return s




    #备注内容
    ####需求、误操作 相关的内容
    # ZMLY-260：需求如此，不更改    -->  .*不.*改
    # ZMLY-218:经过确认，需求已更改，默认不打勾 --> 经.*
    # ZMLY - 221：因操作问题，该问题关闭
    ###重复提交的内容
    # ZMLY-204：该问题在安卓V1.0.2版本出现另外一种现象，见xxxx  -- > .*重复.*见.*
    ###关闭的内容
    #FIRE-150：2020-12- 18 ，测试验证0.4版本：   测试20次以上，没有出现 -- > .*没.*出现.*

    # “活动-备注”内容的判断，主要判断问题关闭时有没有备注
    #TODO 碰上一个问题，备注里面的内容应该是从最新的向最旧的进行过滤，不然会像ZMLY-145，先过滤到第一条就判断正确了。---传过来的文本怎么处理
    #备注内容过滤说明：目前的做法是提取所有内容，然后过滤出要求的关键词就通过
    #更准确的做法：把所有内容按照时间顺序从新到旧排列，然后循环过滤每条评论。如果有重新打开的，需要有大于一条的关闭备注。但是也有误操作重新打开而不是真正有问题重新打开的
    def active_comment_check(self):
        # print(str(self.comment))
        comment = self.comment
        s = ''
        ######检查问题关闭是否填写关闭原因#########
        match1 = ".*关闭.*|验证通过|关闭.*问题|已解决|已修复|未.*现|.*没.*出现.*"
        match_result1 = re.findall(match1, comment)
        if len(match_result1) ==0:
            #过滤不到“正常关闭”的关键词，过滤其他情况
            ######检查问题因 需求或者误操作等 原因的问题#########
            match2 = ".*需求.*|.*操作.*"
            match_result2 = re.findall(match2, comment)
            if len(match_result2) == 0:
                # print("没有需求相关原因说明")
                ######检查问题因 重复提交的 原因的问题#########
                #TODO 如果过滤出重复的，要检查有没有关联链接上来，没有要提示相关责任人关联链接上来
                match3 = ".*重复.*|.*见.*|同"
                match_result3 = re.findall(match3, comment)
                if len(match_result3) == 0 :
                    # print("没有重复提交等原因说明")
                    s += '问题关闭但没有备注关闭原因；'
                    print('问题关闭,没有备注关闭原因，没有需求改动或操作有误，或者问题重复等说明；')
                else:
                    #除了说出相同问题，还要把相同问题的链接放上来   \w表示匹配字母数字及下划线，+表示匹配前一个字符1次或无限次
                    match_xiangtong = "\w-\w"
                    match__xiangtong_result = re.findall(match_xiangtong, comment)
                    # print(match__xiangtong_result)
                    if len(match__xiangtong_result) == 0:
                        s += '问题关闭有说明参考相关bug，但未备注对应的链接；'
                    else:
                        print("有备注参考相关问题的说明")
            else:
                print("需求关系，有说明")
        else:
            print("关闭有说明")
        print("return s = %s"%s)
        return s



    #“活动-所有”的判断，主要判断是不是当前的测试人员本人提交的bug  ---完成
    def active_all_check(self):
        all_link = self.activity_link['所有']
        # print(all_link)
        url = 'http://jira.intretech.com:8080'+str(all_link)
        all_link_analysis = Elementanalysis(url)
        bug_create_author = all_link_analysis.activities_all()
        if bug_create_author == self.reporter:
            # print ("本人创建")
            return True
        else:
            # print("非本人创建")
            return False




    #bug规范性检查逻辑
    def check_item(self):
        nonconformity = ''
        # nonconformity1=''
        responsible = ''
        #问题存在
        if self.issue_exist():
            #判断 “问题详情-类型”是问题点
            if self.type_check():
                # 判断测试组和开发组的bug
                if self.assignee_check() and self.reporter_check():
                    # todo 添加buglist汇总的判断 if self.buglist_title_check()
                    # 判断不是buglist汇总的那条,防止像HTSF-1291这种情况把它过滤成bug了
                    if self.buglist_title_check():
                    # 判断 “问题详情-状态”
                    # 问题解决已关闭，检查测试人员是否备注关闭原因
                        if self.bug_status =="[关闭]":
                            if self.bug_status_type == "[解决]" or self.bug_status_type == "已完成":
                                print("问题状态关闭，解决")
                                #问题关闭的时候，也要再检查一遍测试人员和开发人员填写是否规范
                                ###检查开发人员的填写内容：解决措施+修复版本###
                                assignee_nonconformity_close = str(self.solution_check()) + str(self.fix_version_check())
                                nonconformity += assignee_nonconformity_close
                                print("问题关闭，检查开发人员的不符合项：%s" % assignee_nonconformity_close)
                                if str(self.solution_check()) != '' or str(self.fix_version_check()) != '':
                                    responsible += str(self.assignee_check()) + ';'
                                    print('添加开发为责任人')
                                ###检查测试人员的填写内容：bug描述 + 影响版本 + 问题关闭原因备注###
                                reporter_nonconformity_close = str(self.description_check()) + str(self.affect_version_check()) + str(self.active_comment_check())
                                nonconformity += reporter_nonconformity_close
                                print("问题关闭，检查测试人员的不符合项：%s" % reporter_nonconformity_close)
                                if str(self.description_check()) != '' or str(self.affect_version_check()) != '' or self.active_comment_check():
                                    responsible+=str(self.reporter_check())+';'
                                    print('添加测试人员为责任人')
                                ### 判断该bug是不是测试人员本人提交
                                # 别人转给测试的
                                if self.active_all_check() == False:
                                   if str(self.description_check()) != '' or self.affect_version_check() != ''or self.active_comment_check() != '':
                                        nonconformity += "此bug不是由测试人员创建，但请测试人员尽量补全bug信息; "
                            else:
                                #“问题详情-解决结果”为其他情况，不检查
                                #pass
                                print("问题状态关闭，其他解决方式")
                        # 问题已解决，检查开发人员的解决措施是否填写规范
                        elif self.bug_status == "[解决]":
                            if self.bug_status_type == "[解决]" or self.bug_status_type == "已完成":
                                print("问题状态解决，解决")
                                #检查开发人员填写的解决措施是否填写规范，修复版本是否填写
                                assignee_nonconformity_solute = str(self.solution_check()) + str(self.fix_version_check())
                                nonconformity += assignee_nonconformity_solute
                                if str(self.solution_check()) != '' or str(self.fix_version_check()) != '':
                                    responsible+=str(self.assignee_check())+';'
                            else:
                                # “问题详情-解决结果”为其他情况
                                # pass
                                print("问题状态解决，其他解决方式")
                            # return nonconformity, responsible
                        # “问题详情-状态为 提出、重新打开、正在处理”
                        else:
                            print("问题状态提出，未解决")
                            #检查测试人员提交的bug描述是否规范,是否有填写“影响版本”
                            reporter_nonconformity_open = str(self.description_check()) + str(self.affect_version_check())
                            nonconformity += reporter_nonconformity_open
                            if str(self.description_check()) !='' or str(self.affect_version_check()) != '':
                                responsible+=str(self.reporter_check())+';'
                            ### 判断该bug是不是测试人员本人提交
                            # 别人转给测试的
                            if self.active_all_check() == False:
                                if str(self.description_check()) != '' or str(self.affect_version_check()) != '':
                                    nonconformity += "此bug不是由测试人员创建，但请测试人员尽量补全bug信息; "
                            # return nonconformity, responsible
                        return  nonconformity, responsible
                    # 是buglist汇总的那条，跳过不检查
                    else:
                        return nonconformity, responsible
                #“经办人”不是开发组，“报告人”不是测试组，跳过不检查
                else:
                    print("不是测试组和开发组的bug")#pass 跳过不检查，返回空数组
                    return nonconformity, responsible
            #“问题详情-类型”不是问题点
            else:
                print("问题详情-类型 不是问题点")#pass 跳过不检查，返回空数组
            return nonconformity, responsible
        #问题不存在
        else:
            exist_flag = 0
            print("问题点不存在")
            return nonconformity, responsible



#以下为调试用，不要删除
# b=BusinessLogic('GGXB-5555')

# b.assignee_check()
# b.reporter_check()
# print(b.active_all_check())
# print(b.description_check())
# print(b.comment)
# print(b.fixfor_val)
# print(b.versions_val)
# print(b.buglist_title_check())
# print(b.check_item())
#
# a=[]
# b_check = b.check_item()
# if b_check[0]:
#     print('1')
# else:
#     print("mei")
# print(b.active_comment_check())
# print(b.solution_check())

# match_str1 = "[A-Z]*-[0-9]*"
# match_str3 = ".*重复.*|.*见.*|同"
# match_result1 = re.findall(match_str3, "该问题在安卓V1.0.2版本出现另外一种现象，见：http://jira.intretech.com:8080/browse/ZMLY-282")
# print(match_result1)