# Create your views here.
from .utils import create_hotel, movement_in_hotel, check_power_consuption, no_movement_in_hotel, valid_input
from django.shortcuts import render


def index(request):
    return render(request, "inputs.html")


def home(request):
    return render(request, "index.html")


def inputs(request):
    floor_count = int(request.POST['floor_count'])
    print("floor count is - "+str(floor_count))
    main_corridor_count = int(request.POST['main_corridor_count'])
    print("main corridor count is - " + str(main_corridor_count))
    sub_corridor_count = int(request.POST['sub_corridor_count'])
    print("sub corridor count is - " + str(sub_corridor_count))

    hotel = create_hotel(floor_count, main_corridor_count, sub_corridor_count)
    print(hotel)
    floors_list = []
    main_corridor_list = []
    sub_corridor_list = []
    for floors in range(floor_count):
        floors_list.append("floor" + str(floors))
    for main_corridors in range(main_corridor_count):
        main_corridor_list.append("main_corridors"+str(main_corridors))
    for sub_corridors in range(sub_corridor_count):
        sub_corridor_list.append("sub_corridors"+str(sub_corridors))
    hotel = check_power_consuption(hotel, floors_list, main_corridor_list, sub_corridor_list)
    request.session['hotel'] = hotel
    request.session['floors_list'] = floors_list
    request.session['main_corridor_list'] = main_corridor_list
    request.session['sub_corridor_list'] = sub_corridor_list
    valid_floors_list = floors_list
    valid_sub_corridor_list = sub_corridor_list
    return render(request, "show_hotel.html", {'hotel': hotel,
                                               'floors_list': floors_list,
                                               'main_corridor_list': main_corridor_list,
                                               'sub_corridor_list': sub_corridor_list,
                                               'valid_floors_list': valid_floors_list,
                                               'valid_sub_corridor_list': valid_sub_corridor_list,
                                               'alert': False
                                               })


def movement(request):
    movement_dict = {}
    print("Movement Detected In ")
    floor = (request.POST['floor_id'])
    print("floor : " + str(floor))
    movement_dict['floor'] = floor
    main_corridor = (request.POST['main_corridor_id'])
    if main_corridor != '%':
        print("main corridor : " + str(main_corridor))
        movement_dict['main_corridor'] = main_corridor
    sub_corridor = (request.POST['sub_corridor_id'])
    if sub_corridor != '%':
        print("sub corridor : " + str(sub_corridor))
        movement_dict['sub_corridor'] = sub_corridor

    hotel = request.session['hotel']
    floors_list = request.session['floors_list']
    main_corridor_list = request.session['main_corridor_list']
    sub_corridor_list = request.session['sub_corridor_list']

    hotel = movement_in_hotel(hotel, movement_dict)
    hotel = check_power_consuption(hotel, floors_list, main_corridor_list, sub_corridor_list)
    request.session['hotel'] = hotel
    valid_floors_list = []
    valid_sub_corridor_list = []
    for floors in hotel:
        for k, v in hotel[floors].items():
            if 'sub_corridors' in k:
                if hotel[floors][k]['light']:
                    valid_floors_list.append(floors)
                    valid_sub_corridor_list.append(k)
    print(valid_floors_list)
    print(valid_sub_corridor_list)
    return render(request, "show_hotel.html", {'hotel': hotel,
                                               'floors_list': floors_list,
                                               'main_corridor_list': main_corridor_list,
                                               'sub_corridor_list': sub_corridor_list,
                                               'valid_floors_list': valid_floors_list,
                                               'valid_sub_corridor_list': valid_sub_corridor_list,
                                               'alert': False
                                               })


def no_movement(request):
    print("No Movement Detected In ")
    no_movement_dict = {}
    floor = (request.POST['floor_ids'])
    print("floor : " + str(floor))
    no_movement_dict['floor'] = floor
    sub_corridor = (request.POST['sub_corridor_ids'])
    if sub_corridor != '%':
        print("sub corridor : " + str(sub_corridor))
        no_movement_dict['sub_corridor'] = sub_corridor

    hotel = request.session['hotel']
    floors_list = request.session['floors_list']
    main_corridor_list = request.session['main_corridor_list']
    sub_corridor_list = request.session['sub_corridor_list']
    if valid_input(hotel, no_movement_dict):
        hotel = no_movement_in_hotel(hotel, no_movement_dict)
        hotel = check_power_consuption(hotel, floors_list, main_corridor_list, sub_corridor_list)

        alert = False
    else:
        alert = True
    request.session['hotel'] = hotel
    valid_floors_list = []
    valid_sub_corridor_list = []
    for floors in hotel:
        for k, v in hotel[floors].items():
            if 'sub_corridors' in k:
                if hotel[floors][k]['light']:
                    valid_floors_list.append(floors)
                    valid_sub_corridor_list.append(k)
    return render(request, "show_hotel.html", {'hotel': hotel,
                                               'floors_list': floors_list,
                                               'main_corridor_list': main_corridor_list,
                                               'sub_corridor_list': sub_corridor_list,
                                               'valid_floors_list': valid_floors_list,
                                               'valid_sub_corridor_list': valid_sub_corridor_list,
                                               'alert': alert
                                               })
