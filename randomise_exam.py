#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
title           :randomise_exam.py

description     :Randomises the order of questions and answers
                 in a multiple choice exam created using the exam.tex template
author          :Gareth Roberts, Department of Linguistics,
                 University of Pennsylvania
usage           :python randomise_exam.py (for default)
                 Otherwise import module into python as (e.g., rex)
                 and run rex.make_exams(<filename>,<number of versions>)
python_version  :2.7.7
"""


import random,re,os


class Glbls: #Global variables
    default_filename = "exam.tex"
    default_number = 2
    question_line = re.compile(r'\s*\\q.*')
    answer_line = re.compile(r'\s*\\(fixed)*ans.*')
    fixed_answer_line = re.compile(r'\s*\\fixedans.*')
    end_answer_line = re.compile(r'\s*\\ea.*')
    correct_answer_line = re.compile(r'\s*\\(fixed)*ans.*%correct.*')
    rfoot_line = re.compile(r'\s*\\rfoot.*')
    endofquestions = re.compile(r'\s*%endofquestions.*')
    inquestion = 0
    inquestions = 0
    questions = []
    current_question = []
    current_answers = []
    shuffled_question = []
    
    answers_file = ("answers_file.txt")
    letters = ["A","B","C","D","E","F","G","H","I","J"]
    #Maybe you'll need more than 10 versions of the same exam, but I doubt it.
    



def test(filename):
    f = open(filename,'r')
    for line in f:
        if re.match(Glbls.answer_line,line):
            print line

def randomise(filename,outfile,letter):
    output_file = outfile
    f = open(filename,'r')
    of = open(output_file,'w')
    for line in f:
        if re.match(Glbls.endofquestions,line):
            Glbls.inquestions = 0
            random.shuffle(Glbls.questions)
            for qbundle in Glbls.questions:
                for item in qbundle:
                    of.write(item)
                 
        elif Glbls.inquestion == 1:
            Glbls.current_question.append(line)
        elif (not re.match(Glbls.answer_line,line)
            and not re.match(Glbls.question_line,line)
            and not re.match(Glbls.end_answer_line,line)
            and Glbls.inquestions == 0):
            of.write(line)
            if re.match(Glbls.rfoot_line,line):
                lfoot_line = '\\lfoot{' + letter + '}\n'
                of.write(lfoot_line)
            
        elif re.match(Glbls.question_line,line):
            Glbls.inquestion = 1
            Glbls.inquestions = 1
            Glbls.current_question.append(line)
        
        if re.match(Glbls.end_answer_line,line):
            Glbls.inquestion = 0        
            for l in Glbls.current_question:
                if (not re.match(Glbls.answer_line,l)
                    and not re.match(Glbls.end_answer_line,l)):
                    Glbls.shuffled_question.append(l)
                if re.match(Glbls.answer_line,l):
                    Glbls.current_answers.append(l)
                if re.match(Glbls.end_answer_line,l):
                    fixed = ([(pos, item) for (pos,item) in enumerate(Glbls.current_answers)
                              if re.match(Glbls.fixed_answer_line,item)])
                    random.shuffle(Glbls.current_answers)
                    for pos, item in fixed:
                        index = Glbls.current_answers.index(item)
                        Glbls.current_answers[pos], Glbls.current_answers[index] = Glbls.current_answers[index], Glbls.current_answers[pos]
                    for ans in Glbls.current_answers:
                        Glbls.shuffled_question.append(ans)
                    Glbls.shuffled_question.append(l)
                    Glbls.shuffled_question.append("\n")
                    Glbls.questions.append(Glbls.shuffled_question)
                    Glbls.shuffled_question = []
                    Glbls.current_question = []
                    Glbls.current_answers = []
               
                        
    f.close()
    of.close()
    #xyz.close()
    qnumber = 0
    af = open(Glbls.answers_file,'w')
    af.write("Multiple Choice answers\n")
    for qset in Glbls.questions:
        anumber = -1
        qnumber += 1
        af.write("\n")
        af.write(str(qnumber))
        for qline in qset:
            #print qline
            if re.match(Glbls.answer_line,qline):
                anumber += 1
            if re.match(Glbls.correct_answer_line,qline):
                af.write(Glbls.letters[anumber])
    af.close()

def make_exams(filename,n):
    for i in range(0,n):
        Glbls.inquestion = 0
        Glbls.inquestions = 0
        Glbls.questions = []
        Glbls.current_question = []
        Glbls.current_answers = []
        Glbls.shuffled_question = []
        letter = Glbls.letters[i]
        Glbls.answers_file = "answers_file" + letter + ".txt"
        outfile = "RANDOMISED_" + letter + "_" + filename
        randomise(filename,outfile,letter)
        
        
def run_default():
    files_here = os.listdir(".")
    for f in files_here:
        if f == Glbls.default_filename:
            make_exams(f,Glbls.default_number)
    
run_default()    
            
        
        
    
