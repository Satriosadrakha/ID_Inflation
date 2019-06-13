from math import trunc
from random import randint, uniform
from Forecast_Inflasi import forecast

def prosesGA(timeSeries, pop, chromosome):
    # 3. Evaluasi Chromosome
    #    Pakai Forecasting ANN
    fungsi_objektif = []
    for x in range(0, pop):
        fungsi_objektif.append(forecast(timeSeries,[chromosome[x][0],chromosome[x][1],chromosome[x][2]]))
    average=sum(fungsi_objektif)/pop
#     print("FO = " + str(fungsi_objektif))
    print("Average = " + str(average))
    
    def merge(list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
        return merged_list
    merged = merge(chromosome,fungsi_objektif)
    
    # Python code to sort a list of tuples  
    # according to given key. 

    # get the last key. 
    def last(n): 
        return n[1]   

    # function to sort the tuple    
    def sort(tuples): 

        # We pass used defined function last 
        # as a parameter.  
        return sorted(tuples, key = last) 

    # driver code
    sorted_merged = sort(merged)
#     print("Sorted & merged = " + str(sorted_merged))
    #fungsi_objektif = fungsi_objektif.sort()
    
    #dictionary = dict(zip(chromosome, fungsi_objektif))
    
    #     4. Seleksi Chromosome
    #     Proses seleksi dilakukan dengan cara membuat
    # chromosome yang mempunyai fungsi_objektif kecil mempunyai
    # kemungkinan terpilih yang besar atau mempunyai nilai probabilitas yang tinggi.
    # Untuk itu dapat digunakan fungsi fitness = (1/(1+fungsi_objektif)), fungsi_objektif
    #  perlu ditambah 1 untuk menghindari kesalahan program yang diakibatkan pembagian oleh 0.

#     fitness = []
#     for i in range(0,pop):
#         fitness.append(1/(fungsi_objektif[i]+1))
#     total_fitness= sum(fitness)
    
#     probabilityF = []
#     for i in range(0,pop):
#         probabilityF.append(fitness[i]/total_fitness)
#     # nilai kumulatif
#     C = []
#     C.append(probabilityF[0])
#     for i in range(1,pop):
#         C.append(probabilityF[i-1]+probabilityF[i])
        
#     # Setelah dihitung cumulative probabilitasnya maka proses seleksi menggunakan roulete-wheel dapat dilakukan.
#     # Prosesnya adalah dengan membangkitkan bilangan acak R dalam range 0-1.
#     # Jika R[k] < C[1] maka pilih chromosome 1 sebagai induk, selain itu pilih chromosome ke-k sebagai induk dengan syarat C[k-1] < R < C[k].
#     # Kita putar roulete wheel sebanyak jumlah populasi yaitu 20 kali (bangkitkan bilangan acak R) dan pada tiap putaran, kita pilih satu chromosome untuk populasi baru.
#     print("Chromosome: " + str(chromosome))
    
#     R = []
#     for i in range(0,pop):
#         R.append(uniform(0,1))
#     nChrome =[]
#     for i in range(0,pop):
#         isiGen = []
#         selected = chromosome[pop-1]
#         for j in range(pop-1,-1,-1):
#             if R[i] < C[j]:
#                 selected = chromosome[j]
#         for x in range(0,3):
#             isiGen.append(selected[x])
#         nChrome.append(isiGen)
        
#     print("nChrome: " + str(nChrome))
    
    # 5. Crossover
    # Setelah proses seleksi maka proses selanjutnya adalah proses crossover.
    # Metode yang digunakan salah satunya adalah one-cut point, yaitu memilih secara acak satu posisi dalam chromosome induk kemudian saling menukar gen.
    # Chromosome yang dijadikan induk dipilih secara acak dan jumlah chromosome yang mengalami crossover dipengaruhi oleh parameter crossover_rate  ( ρc ).
    # Dalam satu generasi ada 50% Chromosome dari satu generasi mengalami proses crossover.
    # Prosesnya adalah sebagai berikut:
    parent = []
#     index = []
#     while len(parent) != pop/2:
#         for k in range (0,pop):
#             R[k] = uniform(0,1)
#             # crossover_rate
#             if R[k] < 0.25:
#                 parent.append(nChrome[k])
#                 index.append(k)
#         if len(parent) != pop/2:
#             parent = []
#             index = []
#     print("Parent: " + str(parent))
#     print("Index: " + str(index))
    
    for i in range(0,pop/2):
        parent.append(sorted_merged[i][0])
#     print("Parent = " + str(parent))
#     for x in range(0, pop/2):
    
    nC = []
    for i in range(0,pop):
        nC.append(randint(1,2))
#     print("nC: " + str(nC))
    
    def CrossOver(nC,chromosome1,chromosome2):
        cross = []
        for i in range(0,3):
            if i < nC :
                cross.append(chromosome1[i])
            else:
                cross.append(chromosome2[i])
        return cross
    
    offspring = []
    for j in range(0, int(pop/2)):
        if j == pop/2-1:
            offspring.append(CrossOver(nC[j],parent[j],parent[0]))
        else:
            offspring.append(CrossOver(nC[j],parent[j],parent[j+1]))
            
#     for i,value in enumerate(nChrome):
#         for j in range(0, int(pop/2)):
#             #print(str(i) + " " + str(j))
#             if j == pop/2-1:                
#                 nChrome[i] = CrossOver(nC[j],parent[j],parent[0])
#             elif i == index[j]:
#                 nChrome[i] = CrossOver(nC[j],parent[j],parent[j+1])
    nChrome = parent + offspring
    
    total_gen = 3*pop
    mutation1 = randint(1,total_gen-1)
    mutation2 = mutation1
    while mutation2 == mutation1:
        mutation2 = randint(1,total_gen-1)
    def mutate(mutation):
        if mutation == 0:
            return uniform(0.002, 0.2)
        elif mutation == 1:
            return uniform(0, 0.001)
        else:
            return uniform(0.5, 0.9)
#     print("Mutation1= " + str(mutation1) + "Mutation2= " + str(mutation2))
    nChrome[trunc(mutation1/3)][mutation1%3] = mutate(mutation1%3)
    nChrome[trunc(mutation2/3)][mutation2%3] = mutate(mutation2%3)

    fungsi_objektif = []
    for x in range(0, pop):
        fungsi_objektif.append(forecast(timeSeries,[chromosome[x][0],chromosome[x][1],chromosome[x][2]]))
    average=sum(fungsi_objektif)/pop

    return (nChrome,average)

def GA(timeSeries):
    # 1. Pembentukan chromosome
    # Karena yang dicari adalah nilai learning rate, decay, dan momentum maka variabel tersebut dijadikan sebagai gen-gen pembentuk chromosome. Batasan nilai learning rate adalah bilangan float 0,002 sampai 0,2. Batasan nilai decay adalah bilangan float 0 sampai 0.001. Batasan nilai momentum adalah bilangan float 0,5 sampai 0,9.
    # https://towardsdatascience.com/learning-rate-schedules-and-adaptive-learning-rate-methods-for-deep-learning-2c8f433990d1
    # https://towardsdatascience.com/hyper-parameter-tuning-techniques-in-deep-learning-4dad592c63c8
    chromosome = []
    # 2. Inisialisasi
    # Proses inisialisasi dilakukan dengan cara memberikan nilai awal gen-gen dengan nilai acak sesuai batasan yang telah ditentukan.
    # Misalkan kita tentukan jumlah populasi adalah 20 dan jumlah generasi adalah 10, maka:
    pop = 20
    gen = 10
    
    for i in range(0,pop):
        isiGen = []
        isiGen.append(uniform(0.002, 0.2))
        isiGen.append(uniform(0, 0.001))
        isiGen.append(uniform(0.5, 0.9))
        chromosome.append(isiGen)
    progress = []
    nChromosom, average = prosesGA(timeSeries, pop, chromosome)
    print("Iterasi pertama selesai")
    for x in range(1, gen):
        print("Mulai Iterasi ke-" + str(x + 1))
        nChromosom, average = prosesGA(timeSeries, pop, nChromosom)
        print("Iterasi ke-" + str(x + 1) + ": " + str(nChromosom))
        progress.append(nChromosom)
    print("List terakhir (iterasi ke-" + gen + "): " + str(nChromosom))

    # just some initial value
    bestVal = 1
    bestPop = []
    
    # Menentukan nilai terbaik
    for i in range (0,pop):
        if(forecast(timeSeries,[nChromosom[i][0],nChromosom[i][1],nChromosom[i][2]])<bestVal):
            bestPop = nChromosom[i]
            bestVal = forecast(timeSeries,[nChromosom[i][0],nChromosom[i][1],nChromosom[i][2]])
    print("Chromosome nilai terbaik adalah :" + str(bestPop))
    print("Nilai Terbaik adalah :" + str(bestVal))
    return 0

if __name__ == '__main__':
    GA()