
import os
import glob
import arxiv
import sys
import numpy as np

home_dir = os.environ['HOME']

#-------------------------------------
pdf_folder = home_dir+""
datafol    = "./data/"
output     = "./arxiv.html"
#-------------------------------------

if not os.path.isdir(datafol):
    os.mkdir(datafol)

# get lists
lists_pdf = glob.glob(pdf_folder+"/*.pdf")
lists = []
for i in range(len(lists_pdf)):
    lists += [lists_pdf[i].split("/")[-1].split(".pdf")[0]]

# get data list
lists_exist_pre = glob.glob(datafol+"*.*")
lists_exist = []
for i in range(len(lists_exist_pre)):
    lists_exist += [lists_exist_pre[i].split("/")[-1].split(".pdf")[0]]

make_list = []
rem_list  = []
for lis in lists:
    if not lis in lists_exist:
        make_list += [lis]

for lis in lists_exist:
    if not lis in lists:
        rem_list += [lis]


mis_list = []
for lis in make_list:
    try:
        search = arxiv.Search(id_list=[lis])
        paper = next(search.results())
        names = []
        for i in range(len(paper.authors[:])):
            names += [str(paper.authors[i])]

        f = open(datafol+lis, 'w')
        f.write(paper.title+"\n")
    
        for i in range(len(names)):
            f.write(names[i])
            if i < len(names)-1:
                f.write(", ")
        f.write("\n")
        f.write(paper.summary.replace('\n', ''))
        f.close()
    except:
        mis_list += [lis]

for lis in rem_list:
    os.remove(datafol+lis)

lists  = glob.glob("./data/*")
nlists = []
month  = []
for lis in lists:
    nlists += [lis.split("/")[2]]
for lis in nlists:
    if not lis.split(".")[0] in month:
        month += [lis.split(".")[0]]


f = open(output, "w")
f.write("<script type=\"text/javascript\" async src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML\">\n")
f.write("</script>\n")
f.write("<script type=\"text/x-mathjax-config\">\n")
f.write(" MathJax.Hub.Config({tex2jax: {inlineMath: [[\'$\', \'$\'] ], displayMath: [ [\'$$\',\'$$\'], [\"\\\\[\",\"\\\\]\"] ]}});\n")
f.write("</script>\n")

f.write("<ol>\n")
i = 1
for lis in month:
    f.write("<li><a href=\"#anchor"+str(i)+"\">"+lis+"</a></li>\n")
    i += 1
f.write("<li><a href=\"#anchor"+str(i)+"\">error</a></li>\n")
f.write("</ol>\n")

i =  1
for lis_month in month:
    f.write("<p><a id=\"anchor"+str(i)+"\"></a></p>")

    nums = []
    nums_int = []
    for lis in nlists:
        if lis.split(".")[0] == lis_month:
            nums += [lis.split(".")[1]]
            nums_int += [int(lis.split(".")[1])]

    nums_int = np.array(nums_int)
    nums_int = np.sort(nums_int)

    ii = 1

    for nn in nums_int:
        n = str(nn).zfill(5)
        
        lis = lis_month+"."+n
        num = 0
        for l in open('./data/'+lis).readlines():
            if num == 0:
                f.write("<h2>"+l+"</h2>\n")
                num += 1
            else:
                f.write("<p>"+l+"</p>\n")
        f.write("<p><a href=\"https://arxiv.org/abs/"+str(lis)+"\">arXiv:"+str(lis)+"</a>: <a href=\""+pdf_folder+lis+".pdf\">PDF</a></p>\n")
        f.write("<p> <br> </p>")
        ii+=1
    i+=1

f.write("<h2>error list</h2>\n")
f.write("<p><a id=\"anchor"+str(i)+"\"></a></p>")
for lis in mis_list:
    f.write("<a href=\""+pdf_folder+lis+".pdf\">"+lis+".pdf"+"</a></p>\n")
f.close()





