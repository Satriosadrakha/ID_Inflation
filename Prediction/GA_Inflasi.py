from math import trunc
from random import randint, uniform
from Forecast_Inflasi import forecast

def prosesGA(timeSeries, pop, chromosome, fungsi_objektif):
    # 3. Evaluasi Kromosom
    #    Pakai Forecasting ANN
#     fungsi_objektif = []
#     for x in range(0, pop):
#         fungsi_objektif.append(forecast(timeSeries,[chromosome[x][0],chromosome[x][1],chromosome[x][2]]))
#     average=sum(fungsi_objektif)/pop
#     #print("FO = " + str(fungsi_objektif))
#     print("Rerata = " + str(average))
    
    def merge(list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
        return merged_list
    merged = merge(chromosome,fungsi_objektif)
    
    # 4. Seleksi Kromosom
    # Dari total populasi, ambil 1/2 jumlahnya dengan nilai fungsi objektif yang terbesar 

    def last(n): 
        return n[1]   

    def sort(tuples): 
        return sorted(tuples, key = last) 

    sorted_merged = sort(merged)
    #print("Sorted & merged = " + str(sorted_merged))
    #fungsi_objektif = fungsi_objektif.sort()
    
    # 5. Crossover
    # Setelah proses seleksi maka proses selanjutnya adalah proses crossover.
    # Metode yang digunakan salah satunya adalah one-cut point, yaitu memilih secara acak satu posisi dalam chromosome induk kemudian saling menukar gen.
    # Chromosome yang dijadikan induk dipilih secara acak dan jumlah chromosome yang mengalami crossover dipengaruhi oleh parameter crossover_rate  ( ρc ).
    # Dalam satu generasi ada 50% Chromosome dari satu generasi mengalami proses crossover.
    # Prosesnya adalah sebagai berikut:
    parent = []
    
#     for i in range(0,pop/2):
    for i in range(0,10):
        parent.append(sorted_merged[i][0])
    # print("Parent = " + str(parent))
    
    nC = []
    for i in range(0,pop):
        nC.append(randint(1,2))
    # print("nC: " + str(nC))
    
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
    # print("Mutation1= " + str(mutation1) + "Mutation2= " + str(mutation2))
    nChrome[trunc(mutation1/3)][mutation1%3] = mutate(mutation1%3)
    nChrome[trunc(mutation2/3)][mutation2%3] = mutate(mutation2%3)

    fungsi_objektif = []
    for x in range(0, pop):
        fungsi_objektif.append(forecast(timeSeries,[chromosome[x][0],chromosome[x][1],chromosome[x][2]]))
    average=sum(fungsi_objektif)/pop

    return (nChrome,fungsi_objektif,average)

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
    gen = 2
    
    for i in range(0,pop):
        isiGen = []
        isiGen.append(uniform(0.002, 0.2))
        isiGen.append(uniform(0, 0.001))
        isiGen.append(uniform(0.5, 0.9))
        chromosome.append(isiGen)
        
    progress = []
    
    print("Mulai Iterasi pertama.")
    
    fungsi_objektif = []
    for x in range(0, pop):
        fungsi_objektif.append(forecast(timeSeries,[chromosome[x][0],chromosome[x][1],chromosome[x][2]]))
    average=sum(fungsi_objektif)/pop
    
    print("Rerata awal = " + str(average))
    
#     nChromosom, average = prosesGA(timeSeries, pop, chromosome)
#     print("Nilai rerata iterasi pertama: " + str(average))

    for x in range(0, gen):
        print("Mulai iterasi ke-" + str(x + 1))
        chromosome, fungsi_objektif, average = prosesGA(timeSeries, pop, chromosome, fungsi_objektif)
        print("Nilai rerata iterasi ke-" + str(x + 1) + ": " + str(average))
        progress.append(chromosome)
    print("List terakhir (iterasi ke-" + str(gen) + "): " + str(fungsi_objektif))

    # just some initial value
    bestVal = 1
    bestPop = []
    
    # Menentukan nilai terbaik
    for i in range (0,pop):
        if(forecast(fungsi_objektif[i]<bestVal):
            bestPop = chromosome[i]
            bestVal = fungsi_objektif[i]
    print("Kromosom nilai terbaik adalah : " + str(bestPop))
    print("Nilai Terbaik adalah : " + str(bestVal))
    return (bestPop)

if __name__ == '__main__':
    GA()