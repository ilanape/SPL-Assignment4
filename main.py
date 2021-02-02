import sys
from DTO import Vaccine, Supplier, Clinic, Logistic

from Repository import repo

def main(argv):
    repo.create_tables()

    # config file parser
    config = open(argv[1], 'r')
    first_line = config.readline().replace("\n","").split(',')
    num_of_vaccines = (int(first_line[0]))
    num_of_suppliers = (int(first_line[1]))
    num_of_clinics = (int(first_line[2]))
    num_of_logistics = (int(first_line[3]))

    while num_of_vaccines != 0:
        line = config.readline().replace("\n","").split(',')
        repo.vaccines.insert(Vaccine((int(line[0])),date_fix(line[1]), (int(line[2])), (int(line[3]))))
        num_of_vaccines = num_of_vaccines - 1

    while num_of_suppliers != 0:
        line = config.readline().replace("\n","").split(',')
        repo.suppliers.insert(Supplier((int(line[0])), line[1], (int(line[2]))))
        num_of_suppliers = num_of_suppliers - 1

    while num_of_clinics != 0:
        line = config.readline().replace("\n","").split(',')
        repo.clinics.insert(Clinic((int(line[0])), line[1], (int(line[2])), (int(line[3]))))
        num_of_clinics = num_of_clinics - 1

    while num_of_logistics != 0:
        line = config.readline().replace("\n","").split(',')
        repo.logistics.insert(Logistic((int(line[0])), line[1], (int(line[2])), (int(line[3]))))
        num_of_logistics = num_of_logistics - 1

    config.close()

    # orders file parser
    orders = open(argv[2], 'r')
    output = open(argv[3], 'w')
    lines = orders.readlines()

    for line in lines:
        split_list = line.replace("\n","").split(',')
        if split_list.__len__() == 3:
            receive_shipment(split_list[0], (int(split_list[1])), date_fix(split_list[2]))
        else:
            send_shipment(split_list[0], (int(split_list[1])))

        #write to output
        s = str(repo.vaccines.total_inventory()) + ',' + str(repo.clinics.total_demand()) + ',' + str(repo.logistics.total_received()) + ',' + str(repo.logistics.total_sent()) + "\n"
        output.write(s)

    orders.close()
    output.close()


def receive_shipment(name, amount, date):
    supplier = repo.suppliers.find_by_name(name)
    new_vaccine = Vaccine(repo.vaccines.find_index(), date, supplier.id, amount)
    repo.vaccines.insert(new_vaccine) #add vaccine to inventory
    repo.logistics.update_count_received(supplier.logistic, amount) #update the logistic count received


def send_shipment(location, amount):
    clinic = repo.clinics.find_by_location(location)
    repo.clinics.reduce_amount_demand(clinic.id, amount) #reduce the demand from the clinic
    repo.vaccines.remove_amount_inventory(amount) #take the demand from inventory
    repo.logistics.update_count_sent(clinic.logistic, amount) #update the logistic count sent

def date_fix(date):
    if date.__len__()==9:
        date= date[:8] + '0' + date[8:]
    return date


if __name__ == '__main__':
    main(sys.argv)


