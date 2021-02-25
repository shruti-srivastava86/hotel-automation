import datetime as dt


def is_now_in_night_time(now_time):
    start_time = dt.time(18, 00)
    end_time = dt.time(6, 00)
    if now_time >= start_time or now_time <= end_time:
        return True
    return False


class Hotel:
    def __init__(self, fc, mcc, scc):
        self.fc = fc
        self.mcc = mcc
        self.scc = scc

    def build(self):
        hotel_dict = {}
        for floors in range(self.fc):
            hotel_dict["floor" + str(floors)] = {}
            for main_corridors in range(self.mcc):
                if is_now_in_night_time(dt.datetime.now().time()):
                    hotel_dict["floor" + str(floors)]["main_corridors"+str(main_corridors)] = {'light': True,
                                                                                               'AC': True}
                else:
                    hotel_dict["floor" + str(floors)]["main_corridors" + str(main_corridors)] = {'light': False,
                                                                                                 'AC': True}
            for sub_corridors in range(self.scc):
                hotel_dict["floor" + str(floors)]["sub_corridors"+str(sub_corridors)] = {'light': False, 'AC': True}
        return hotel_dict


def create_hotel(fc, mcc, scc):
    hotel = Hotel(fc, mcc, scc)
    return hotel.build()


def movement_in_hotel(hotel, movement_dict):
    print(hotel)
    change_line = hotel[movement_dict['floor']]
    for keys in change_line:
        print(keys)
        if keys in movement_dict.values():
            change_line[keys]['light'] = True
            change_line[keys]['AC'] = True
        else:
            change_line[keys]['AC'] = False
    print(change_line)
    hotel[movement_dict['floor']] = change_line
    return hotel


def check_power_consuption(hotel, floors_list, main_corridor_list, sub_corridor_list):
    main_corridors = len(floors_list)*len(main_corridor_list)
    sub_corridors = len(floors_list)*len(sub_corridor_list)
    total_allowable_power = (15*main_corridors) + (10*sub_corridors)
    power_consumed = 0
    for floors in hotel:
        for corridors in hotel[floors]:
            if hotel[floors][corridors]['light']:
                power_consumed += 5
            if hotel[floors][corridors]['AC']:
                power_consumed += 10
    if power_consumed > total_allowable_power:
        for floors in hotel:
            for keys in hotel[floors]:
                if 'sub_corridors' in keys:
                    if hotel[floors][keys]['AC']:
                        hotel[floors][keys]['AC'] = False
    return hotel


def no_movement_in_hotel(hotel, movement_dict):
    change_line = hotel[movement_dict['floor']]
    for keys in change_line:
        if keys in movement_dict.values():
            change_line[keys]['light'] = False
            change_line[keys]['AC'] = True
    hotel[movement_dict['floor']] = change_line
    return hotel


def valid_input(hotel, no_movement_dict):
    if hotel[no_movement_dict['floor']][no_movement_dict['sub_corridor']]['light']:
        return True
    return False

