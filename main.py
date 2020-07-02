import numpy as np
import random as rd

class Client:

    def __init__(self, actual_time):
        self.quantity_products = int(UniformInstance(1,50))
        self.state = "Llegada"
        self.queue_time = "No"
        self.looking_for = actual_time + ExponentialInstance(1/5)
        self.queue_start = 0
        self.queue_finish = 0
        

    def discount_product (self):
        self.quantity_products -= 1

 
class Cashier:

    def __init__(self, num, a, b, lambd):
        self.state = 0
        self.num = num
        self.a = 0
        self.b = 0
        self.lambd = 0

    def change_params(self, a, b, lambd):
        self.a = a
        self.b = b
        self.lambd = lambd

    def generate_next_product_attendance(self, actual_time):
        if self.num == 1 or self.num == 3:
            return actual_time + UniformInstance(self.a, self.b)
        else:
            return actual_time + ExponentialInstance(self.lambd)


def get_next_event(client1_next_product, client2_next_product, client3_next_product, next_client_at, client_looking_for ):
    if client_looking_for != []:
        return min([client_looking_for[0].looking_for, client1_next_product, client2_next_product, client3_next_product, next_client_at])
    else:
        return min([client1_next_product, client2_next_product, client3_next_product, next_client_at])

    
def ExponentialInstance(lambd):
    return -np.log(1 - np.random.uniform(0,1))/lambd


def UniformInstance(a, b):
   return (b-a)*np.random.uniform(0,1) + a


def DaySimulation():
    
    # initial params of clients arrives
    client_rate_a = 2*60
    client_rate_b = 3*60
    client_rate_lambda = 0
    
    next_client_at = UniformInstance(client_rate_a,client_rate_b)

    # time in simulation, max and actual
    max_time = 12*60*60
    actual_time = 0

    # data for analysis 
    attended_client = []
    lost_clients = 0
    empty = 0
    empty_last_update = 0
    full_cashers = 0
    full_cashers_last_update = 0
    long_queue_time = {}
    long_queue_recurrence = {}
    for i in range(0,28):
        long_queue_time[i] = 0
        long_queue_recurrence[i] = 0
    last_update_queue = 0
    
    # client next product processed by cashier
    client1_next_product = max_time +1 
    client2_next_product = max_time +1
    client3_next_product = max_time +1

    # cashier class to simulate next product processed
    cashier1 = Cashier(1, 5, 11, 0)
    cashier2 = Cashier(2, 0, 0, 1/6)
    cashier3 = Cashier(3, 4, 16, 0)

    # client assigned in casher  
    client1_in_casher = None
    client2_in_casher = None
    client3_in_casher = None
    
    # list of clients in system, queue and looking for 
    queue_client_list = []
    client_looking_for = []
    

    # start simulation
    while actual_time < max_time:

        client_looking_for = sorted(client_looking_for, key = lambda client: client.looking_for)
        next_event = get_next_event(client1_next_product, client2_next_product, client3_next_product, next_client_at, client_looking_for )
        
        # arrive a client
        if next_event == next_client_at:
            n = 0
            if client1_in_casher != None:
                n += 1
            if client2_in_casher != None:
                n += 1
            if client3_in_casher != None:
                n += 1
            actual_time = next_event
            client = Client(actual_time)
            if len(client_looking_for) + len(queue_client_list)+ n < 30:
                #print("Ha llegado un cliente al sistema")
                client_looking_for.append(client)
            else:
                lost_clients += 1
            
            if actual_time >= 2*60*60 and actual_time <= 6*60*60:
                client_rate_a = 0
                client_rate_b = 0
                client_rate_lambda = 1/60
                next_client_at = actual_time + ExponentialInstance(client_rate_lambda)
                
            else:
                if actual_time > 6*60*60:
                    client_rate_a = 1*60
                    client_rate_b = 2*60
                    client_rate_lambda = 0
                else:
                    client_rate_a = 2*60
                    client_rate_b = 3*60
                    client_rate_lambda = 0
                next_client_at = actual_time + UniformInstance(client_rate_a, client_rate_b)

        # first casher process a product
        elif next_event == client1_next_product:
            
            actual_time = next_event
            #print("Cajero 1 procesa un producto en:\t\t ", actual_time)
            client1_in_casher.quantity_products -= 1
            if client1_in_casher.quantity_products == 0:
                #print("Se terminó de atender el cliente en el cajero 1\t", actual_time)
                attended_client.append(client1_in_casher)
                if client1_in_casher.queue_start != 0:
                    client1_in_casher.queue_finish = actual_time

                if queue_client_list != []:

                    # update queue data
                    long_queue_time[len(queue_client_list)] += actual_time - last_update_queue
                    last_update_queue = actual_time
                    long_queue_recurrence[len(queue_client_list)] += 1
                    
                    client1_in_casher = queue_client_list.pop(0)
                    
                    if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                        cashier1.change_params(10, 20, 0)
                    elif actual_time > 10*60*60:
                        cashier1.change_params(10, 30, 0)
                    else:
                        cashier1.change_params(5, 11, 0)
                        
                    client1_next_product = cashier1.generate_next_product_attendance(actual_time)
                else:
                    client1_next_product = max_time +1
                    client1_in_casher = None
            else:
                if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                    cashier1.change_params(10, 20, 0)
                elif actual_time > 10*60*60:
                    cashier1.change_params(10, 30, 0)
                else:
                    cashier1.change_params(5, 11, 0)
                client1_next_product = cashier1.generate_next_product_attendance(actual_time)
                    
        # second casher process a product    
        elif next_event == client2_next_product:

            actual_time = next_event
            #print("Cajero 2 procesa un producto en:\t\t ", actual_time)
            client2_in_casher.quantity_products -= 1
            if client2_in_casher.quantity_products == 0:
                #print("Se terminó de atender el cliente en el cajero 2\t", actual_time)
                attended_client.append(client2_in_casher)
                if client2_in_casher.queue_start != 0:
                    client2_in_casher.queue_finish = actual_time

                if queue_client_list != []:

                    # update queue data
                    long_queue_time[len(queue_client_list)] += actual_time - last_update_queue
                    last_update_queue = actual_time
                    long_queue_recurrence[len(queue_client_list)] += 1
                    
                    client2_in_casher = queue_client_list.pop(0)

                    if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                        cashier2.change_params(0, 0, 1/10)
                    elif actual_time > 10*60*60:
                        cashier2.change_params(0, 0, 1/15)
                    
                    client2_next_product = cashier2.generate_next_product_attendance(actual_time)
                else:
                    client2_next_product = max_time +1
                    client2_in_casher = None
            else:
                if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                    cashier2.change_params(0, 0, 1/10)
                elif actual_time > 10*60*60:
                    cashier2.change_params(0, 0, 1/15)
                
                client2_next_product = cashier2.generate_next_product_attendance(actual_time)

        # second casher process a product    
        elif next_event == client3_next_product:
            
            actual_time = next_event
            #print("Cajero 3 procesa un producto en:\t\t ", actual_time)
            client3_in_casher.quantity_products -= 1
            if client3_in_casher.quantity_products == 0:
                #print("Se terminó de atender el cliente en el cajero 3\t", actual_time)
                attended_client.append(client3_in_casher)
                if client3_in_casher.queue_start != 0:
                    
                    client3_in_casher.queue_finish = actual_time
                    
                if queue_client_list != []:
                    
                    # update queue data
                    long_queue_time[len(queue_client_list)] += actual_time - last_update_queue
                    last_update_queue = actual_time
                    long_queue_recurrence[len(queue_client_list)] += 1
                    
                    client3_in_casher = queue_client_list.pop(0)

                    if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                        cashier3.change_params(6, 18, 0)
                    elif actual_time > 10*60*60:
                        cashier3.change_params(10, 22, 0)
                    else:
                        cashier3.change_params(4, 16, 0)
                    client3_next_product = cashier3.generate_next_product_attendance(actual_time)
                else:
                    client3_next_product = max_time +1
                    client3_in_casher = None
            else:
                if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                    cashier3.change_params(6, 18, 0)
                elif actual_time > 10*60*60:
                    cashier3.change_params(10, 22, 0)
                else:
                    cashier3.change_params(4, 16, 0)
                client3_next_product = cashier3.generate_next_product_attendance(actual_time)
                #print("Tiempo de la exponencial" , cashier3.generate_next_product_attendance(5))

        # a client finish to looking for the products
        else:
            actual_time = next_event
            # add client to queue or assign to a casher
            casher_free = []
            if client1_in_casher == None:
                casher_free.append(1)
            if client2_in_casher == None:
                casher_free.append(2)
            if client3_in_casher == None:
                casher_free.append(3)
            # select chaser random
            if casher_free != []:
                casher_assigment = rd.choice(casher_free)
                if casher_assigment == 1:
                    #print("Se asignó un cliente al cajero 1\t\t\t", actual_time)
                    client1_in_casher = client_looking_for.pop(0)
                    if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                        cashier1.change_params(10, 20, 0)
                    elif actual_time > 10*60*60:
                        cashier1.change_params(10, 30, 0)
                    else:
                        cashier1.change_params(5, 11, 0)
                    client1_next_product = cashier1.generate_next_product_attendance(actual_time) 

                elif casher_assigment == 2:
                    #print("Se asignó un cliente al cajero 2\t\t\t", actual_time)
                    client2_in_casher = client_looking_for.pop(0)
                    if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                        cashier2.change_params(0, 0, 1/10)
                    elif actual_time > 10*60*60:
                        cashier2.change_params(0, 0, 1/15)
                    else:
                        cashier2.change_params(0, 0, 1/6)
                    client2_next_product = cashier2.generate_next_product_attendance(actual_time) 

                else:
                    #print("Se asignó un cliente al cajero 3\t\t\t", actual_time)
                    client3_in_casher = client_looking_for.pop(0)
                    if actual_time >= 4*60*60 and actual_time <= 10*60*60:
                        cashier3.change_params(6, 18, 0)
                    elif actual_time > 10*60*60:
                        cashier3.change_params(10, 22, 0)
                    else:
                        cashier3.change_params(4, 16, 0)
                    client3_next_product = cashier3.generate_next_product_attendance(actual_time) 
            else:

                # update queue data
                long_queue_time[len(queue_client_list)] += actual_time - last_update_queue
                last_update_queue = actual_time
                long_queue_recurrence[len(queue_client_list)] += 1
                
                client = client_looking_for.pop(0)
                client.queue_start = actual_time
                queue_client_list.append(client)

        if client1_in_casher == None and client2_in_casher == None and client3_in_casher == None:
            empty += actual_time - empty_last_update
            empty_last_update = actual_time
        else:
            empty_last_update = actual_time
            
        if client1_in_casher != None and client2_in_casher != None and client3_in_casher != None:
            full_cashers += actual_time - full_cashers_last_update
            full_cashers_last_update = actual_time
        else:
            full_cashers_last_update = actual_time
        
        if next_event >= 12*60*60:
            #print("Fin de la simulación")
            n = 0
            queue_time = 0

            # queue mean for a client
            for i in attended_client:
                if i.queue_finish - i.queue_start != 0:
                    queue_time += i.queue_finish - i.queue_start
                    n += 1
            queue_mean = queue_time/n

            # mean long queue
            mean_queue_long = 0
            s = 0
            for key in list(long_queue_time.keys()):
                s += long_queue_time[key]            
            for key in list(long_queue_time.keys()):
                mean_queue_long += key * long_queue_time[key] / s

            #print(empty)
            #print(full_cashers/(12*60*60))
            
            return (len(attended_client), queue_mean, mean_queue_long, empty, full_cashers/(12*60*60), lost_clients) 
        
def simlations():
    attended_clients = []
    queue_means = []
    mean_queue_longs = []
    emptys = []
    fully_cashers = []
    lost_clients = []
    for i in range(100):
        a,b,c,d,e,f = DaySimulation()
        attended_clients.append(a)
        queue_means.append(b)
        mean_queue_longs.append(c)
        emptys.append(d)
        fully_cashers.append(e)
        lost_clients.append(f)
    print(np.mean(attended_clients))
    print(np.mean(queue_means))
    print(np.mean(mean_queue_longs))
    print(np.mean(emptys))
    print(np.mean(fully_cashers))
    print(np.mean(lost_clients))


print(simlations())












    
