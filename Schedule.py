

total_hours=8
chunk_list=[]

#utility function: takes task, divides it into requisite number of pieces according to time
def build_chunks(task_list):
    for task in task_list.keys():
      #  print(task)
        time_chunks=task_list[task]
        for index in range(time_chunks[1]):
            duration=(int)(time_chunks[0]/time_chunks[1])
            chunk_list.append([task,1/time_chunks[1], duration])
    #print (chunk_list)

#goes through the permutations, step by step until the total equals (returns the current list) or exceeds (returns none) the total goal hours
def get_acceptable_list(task_permutation):
    total_time=0
    candidate_list=[]
    #print (task_permutation)
    for task in task_permutation: 
        if (task[1]+total_time)<=total_hours: #Will this put us above total hours? 
           total_time+=task[2]
           candidate_list.append(task)
           if total_time==total_hours:
               return candidate_list
        else:
            return None

#Basic permutation function
def permute_chunks(chunks):
    output=[]
    if len(chunks)==1:
        return chunks
    else:
        for index, chunk in enumerate(chunks):
            for permutation in permute_chunks(chunks[:index] + chunks[index+1:]):
                output+=list([chunk+permutation])
    return output


#Because the permutation function breaks down data structures in the "+" and we need to recombine them into Task/Completion%/Time units
#Alternatively, we could have just permuted a list of names (1 per chunk--not task) and then accessed the original dictionary data for time info
def rebuild_triplets(fused_chunks):
    output=[]
    index=0
    while (index+1<(len(fused_chunks))):
        task_unit=[fused_chunks[index],fused_chunks[index+1],fused_chunks[index+2]]
        index+=3
        output.append(task_unit)
    return (output)


#Name is key, then a three figure tuple: total time, numsegments, priority (for later):
# "F": Must finish "I": Must Include  "N": No urgency
sample_data={"Board Meeting":(3,1,"F"),"Email":(4,2,"I"), "Debug":(6,2,"N"),"Rewrite resume":(3,1), "Clean bathrooms":(4,2), "Heart surgery": (5,1)} 

build_chunks(sample_data)
permu_chunks=permute_chunks(chunk_list)
print ("Num tasks:", len(sample_data), " ,divided into ", len(chunk_list), " chunks yielding ", (int)(len(permu_chunks)/3), " permutations.")
prelim_schedules=[]
final_schedules=[]
for fused_chunk in permu_chunks:
    prelim_schedules.append(rebuild_triplets(fused_chunk))

for schedule in prelim_schedules:
    finalist=get_acceptable_list(schedule)
    if finalist is not None and finalist not in final_schedules: #Because the 'stop when we've filled time' method of checking schedules leads to repeats
        final_schedules.append(finalist)
print ("Total qualifying schedules:", len(final_schedules))
print ("Each task: name, fraction of completion, time taken")
for schedule in final_schedules:
    print(schedule)

