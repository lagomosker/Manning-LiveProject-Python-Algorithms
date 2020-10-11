

total_hours=8
#Name is key, then a three figure tuple: total time, numsegments, priority (for later):
# "F": Must finish "I": Must Include  "N": No urgency
task_list={"Board Meeting":(3,1,"F"),"Email":(4,2,"I"), "Debug":(6,2,"N"),"Rewrite resume":(2,1), "Clean bathrooms":(4,2), "Heart surgery": (5,1)} 
chunk_list=[]
prelim_schedules=[]
final_schedules=[]

#utility function in case they load intasks from a drive
def build_chunks():
    for task in task_list.keys():
        print(task)
        time_chunks=task_list[task]
        for index in range(time_chunks[1]):
            duration=(int)(time_chunks[0]/time_chunks[1])
            chunk_list.append((task,index+1, duration))
    print (chunk_list)

#starts adding up tasks and 
def get_acceptable_list(task_permutation):
    total_time=0
    candidate_list=[]
    for task in task_permutation: 
        if (task[1]+total_time)<=total_hours: #Will this put us above total hours? 
           total_time+=task[1]
           candidate_list.append(task)
           if total_time==total_hours:
               return candidate_list
        else:
            return None

def permute_chunks(chunks):
    output=[]
  #  print(chunks)
    if len(chunks)==1:
        return chunks
    else:
        for index, chunk in enumerate(chunks):
            for permutation in permute_chunks(chunks[:index] + chunks[index+1:]):
                output+=[chunk + permutation]
    return output


build_chunks()
candidates=permute_chunks(chunk_list)
print (len(chunk_list),len(candidates))
#for cand in candidates:
print (cand)
