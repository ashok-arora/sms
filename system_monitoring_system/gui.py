import PySimpleGUI as sg
import core
import keyring
import report

def layout(g, settings):
    cpu_dict = g.cpu()
    memory_dict = g.memory()
    networks = g.network()
    storages = g.storage()
    swap_dict = g.swap()
    users = g.users()
    processes = g.process()

    main_menu = [
        [sg.Text("Overall Usage Summary - ", font=('Montserrat', 10, 'bold'))],
        [sg.Text("Operating System: ", font=('Montserrat', 10, 'bold')), sg.Text(g.os())],
        [sg.Text("Uptime: ", font=('Montserrat', 10, 'bold')), sg.Text("{} seconds".format(g.uptime()), key='-update-')],
        
        [sg.Text("\nCPU - ", font=('Montserrat', 10, 'bold'))], 
        [sg.Text("Load Average: ", font=('Montserrat', 10, 'bold')), sg.Text('{}  {}  {}'.format(cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2]))],

        [sg.Text("User: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['user']))],
        [sg.Text("System: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['system']))],
        [sg.Text("Idle: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['idle']))],
        [sg.Text("I/O Wait: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['iowait']))],
        [sg.Text("Cores: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(cpu_dict['num_cores']))],
  
        [sg.Text("\nMemory - ", font=('Montserrat', 10, 'bold'))], 
        [sg.Text("Total", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['total']))],
        [sg.Text("Used: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['used_incl']))],
        [sg.Text("Free: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['free'])  )],
        
    ]   
    
    # [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],

    main_menu += [ [sg.Text("\nNetwork - ", font=('Montserrat', 10, 'bold'))] ] 

    for network_dict in networks:
        main_menu += [
            [sg.Text("Interface: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['interface']))],
            [sg.Text("IP: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['ip']))],
            [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        ]
    
    main_menu += [ [sg.Text("\nStorage - ", font=('Montserrat', 10, 'bold'))] ] 
    for storage_dict in storages:
        main_menu += [
            [sg.Text("Device: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(storage_dict['device']))],
            [sg.Text("Mounted: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(storage_dict['mountpoint']))],
            [sg.Text("Total: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(storage_dict['total']))],
            [sg.Text("Used: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes ({}%)'.format(storage_dict['used'], storage_dict['percent']))],
            [sg.Text("Free: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(storage_dict['free']))],
            [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        ]
    
    main_menu += [ [sg.Text("\nSwap - ", font=('Montserrat', 10, 'bold'))] ] 
    main_menu += [
        [sg.Text("Total ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['total']))],
        [sg.Text("Used: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes ({}%)'.format(swap_dict['used'], swap_dict['percent']))],
        [sg.Text("Free: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['free']))],
        [sg.Text("Swapped in: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['sin']))],
        [sg.Text("Swapped out: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['sout']))],
        # [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
    ]   

    main_menu += [ [sg.Text("\nUsers - ", font=('Montserrat', 10, 'bold'))] ] 
    for user_dict in users:
        main_menu += [
            [sg.Text("Name: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(user_dict['name']))],
            [sg.Text("Session started: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(user_dict['sess_started']))],
            [sg.Text("Host: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(user_dict['host']))],
            [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        ]
        
    main_menu = [[sg.Column(main_menu, scrollable=True, vertical_scroll_only=True, size=(1000,650))]] + [[
            sg.Button("Generate report", key='-report-main-'),
            sg.Button("Send report as email",key='-email-main-'),
        ]]

    
    cpu_menu = [
        [sg.Text("CPU Usage Summary -", font=('Montserrat', 10, 'bold'))],        
        [sg.Text("Load Average: ", font=('Montserrat', 10, 'bold')), sg.Text('{}  {}  {}'.format(cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2]))],
        [sg.Text("User: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['user']))],
        [sg.Text("System: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['system']))],
        [sg.Text("Idle: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['idle']))],
        [sg.Text("I/O Wait: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['iowait']))],
    ]

    counter = 1
    for cpu_core in cpu_dict['cores']:
        cpu_menu += [
            [sg.Text("Core: ", font=('Montserrat', 10, 'bold')), sg.Text('Core {}:-'.format(counter))],
            [sg.Text("User: ", font=('Montserrat', 10, 'bold')), sg.Text('User: {} %'.format(cpu_core['user']))],
            [sg.Text("System: ", font=('Montserrat', 10, 'bold')), sg.Text('System: {} %'.format(cpu_core['system']))],
            [sg.Text("Idle: ", font=('Montserrat', 10, 'bold')), sg.Text('Idle: {} %'.format(cpu_core['idle']))],
            [sg.Text("I/O Wait: ", font=('Montserrat', 10, 'bold')), sg.Text('I/O Wait: {} %'.format(cpu_core['iowait']))],
            [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        ]
        counter += 1
    
    cpu_menu = [[sg.Column(cpu_menu, scrollable=True, vertical_scroll_only=True, size=(1000,650))]] + [[
        sg.Button("Generate report", key='-report-cpu-'),
        sg.Button("Send report as email",key='-email-cpu-'),
    ]]


    memory_menu = [
        [sg.Text("Memory Usage Summary -", font=('Montserrat', 10, 'bold'))],
    ]
    memory_menu += [
        [sg.Text("Total: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['total']))],
        [sg.Text("Available: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['available']))],
        [sg.Text("Used (excl. Cache & buffer): ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes ({}%)'.format(memory_dict['used_excl'], memory_dict['percent']))],
        [sg.Text("Used (incl. Cache & buffer): ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['used_incl']))],
        [sg.Text("Free: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['free']))],

    ]
    memory_menu = [[sg.Column(memory_menu, scrollable=True, vertical_scroll_only=True, size=(1000,650))]] + [[
        sg.Button("Generate report", key='-report-mem-'),
        sg.Button("Send report as email",key='-email-mem-'),
    ]]

    process_menu = [
        [sg.Text("Process Usage Summary -", font=('Montserrat', 10, 'bold'))],
    ]

    for i in range(10):
        try:
            process_dict = next(processes)
            process_menu += [
                [sg.Text("PID: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(process_dict['pid']))],
                [sg.Text("Name: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(process_dict['name']))],
                [sg.Text("User: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(process_dict['user']))],
                [sg.Text("Status: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(process_dict['status']))],
                [sg.Text("Created: ", font=('Montserrat', 10, 'bold')), sg.Text('{} seconds since the epoch'.format(process_dict['created']))],
                [sg.Text("Memory: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(process_dict['memory']))],
                [sg.Text("CPU: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(process_dict['cpu']))],
                [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
            ]
        except StopIteration:
            break
        
    process_menu = [[sg.Column(process_menu, scrollable=True, vertical_scroll_only=True, size=(1000,650))]] + [[
        sg.Button("Generate report", key='-report-proc-'),
        sg.Button("Send report as email", key='-email-proc-'),
    ]]

    storage_menu = [
        [sg.Text("Storage Usage Summary -", font=('Montserrat', 10, 'bold'))],
    ]       
    for storage_dict in storages:
        storage_menu += [
            [sg.Text("Device: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(storage_dict['device']))],
            [sg.Text("Mounted: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(storage_dict['mountpoint']))],
            [sg.Text("Type: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(storage_dict['fstype']))],
            [sg.Text("Options: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(storage_dict['options']))],
            [sg.Text("Total: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(storage_dict['total']))],
            [sg.Text("Used: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes ({}%)'.format(storage_dict['used'], storage_dict['percent']))],
            [sg.Text("Free: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(storage_dict['free']))],
            [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        ]
    storage_menu = [[sg.Column(storage_menu, scrollable=True, vertical_scroll_only=True, size=(1000,650))]] + [[
        sg.Button("Generate report", key='-report-storage-'),
        sg.Button("Send report as email", key='-email-storage-'),
    ]]

    network_menu = [
        [sg.Text("Network Usage Summary -", font=('Montserrat', 10, 'bold'))],
    ]
    for network_dict in networks:
        network_menu += [
            [sg.Text("Interface: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['interface']))],
            [sg.Text("IP: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['ip']))],
            [sg.Text("Bytes sent: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['bytes_sent']))],
            [sg.Text("Bytes received: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['bytes_recv']))],
            [sg.Text("Packets sent: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['packets_sent']))],
            [sg.Text("Packets received: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['packets_recv']))],
            [sg.Text("Errors in: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['errin']))],
            [sg.Text("Dropped in: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['dropin']))],
            [sg.Text("Dropped out: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(network_dict['dropout']))],
            [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],

        ]
    network_menu = [[sg.Column(network_menu, scrollable=True, vertical_scroll_only=True, size=(1000,650))]] + [[
        sg.Button("Generate report", key='-report-net-'),
        sg.Button("Send report as email", key='-email-net-'),
    ]]

    misc_menu = [
        [sg.Text("Miscellaneous Usage Summary -", font=('Montserrat', 10, 'bold'))],
    ]
    misc_menu += [
        [sg.Text("OS: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(g.os()))],
        [sg.Text("Uptime: ", font=('Montserrat', 10, 'bold')), sg.Text('{} seconds'.format(g.uptime()))],
    ]
    for user_dict in users:
        misc_menu += [
            [sg.Text("Name: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(user_dict['name']))],
            [sg.Text("Session started: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(user_dict['sess_started']))],
            [sg.Text("Host: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(user_dict['host']))],
            [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        ]
    misc_menu += [
        [sg.Text("Total: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['total']))],
        [sg.Text("Used: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes ({}%)'.format(swap_dict['used'], swap_dict['percent']))],
        [sg.Text("Free: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['free']))],
        [sg.Text("Swapped in: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['sin']))],
        [sg.Text("Swapped out: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(swap_dict['sout']))],
       #  [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],

    ]      
    misc_menu = [[sg.Column(misc_menu, scrollable=True, vertical_scroll_only=True, size=(1000,650))]] + [[
        sg.Button("Generate report", key='-report-misc-'),
        sg.Button("Send report as email", key='-email-misc-'),
    ]]

    # names = settings.get("names", ["None"])
    # email = settings.get("email", ["None"])
    # name_email = [n+" - "+e for n, e in zip(names, email)]
    # settings.set("name-email", name_email)
    # name_email = settings.get("email", {"None":"No data found"}).items()

    name_email = settings.get("email", None)
    if name_email is None:
        n_e = ["File doesn't exist - No record found"]
    else: n_e = [n+' - '+e for e, n in name_email.items()]

    settings = [
        # [sg.Text("Its the settings menu")],
        [sg.Text("Current name(s) - email(s): "), sg.Listbox(
            n_e, key="-email-", size=(100, 10), enable_events=True)],
        [
            sg.Button("Set notification limit"),
            sg.Button("Change record"),
            sg.Button("Delete record"),
            sg.Button("Add record"),
            sg.Button("Change password"),
        ],
    ]

    layout = [
        [sg.T("")],
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Main Menu", main_menu, element_justification='center'),
                        sg.Tab("CPU Menu", cpu_menu, element_justification='center'),
                        sg.Tab("Memory Menu", memory_menu, element_justification='center'),
                        sg.Tab("Process Menu", process_menu, element_justification='center'),
                        sg.Tab("Storage Menu", storage_menu, element_justification='center'),
                        sg.Tab("Network Menu", network_menu, element_justification='center'),
                        sg.Tab("Misc Menu", misc_menu, element_justification='center'),
                        sg.Tab("Settings Menu", settings, element_justification='center'),
                    ]
                ],
                border_width=5,
                pad=100,
                enable_events=True,
            )
        ],
    ]

    window = sg.Window(
        "System Monitoring System", layout, size=(1000, 800),
        element_justification="c"
    )
    # window["abc"].Widget.configure(highlightcolor='red',
    # highlightthickness=2)
    return window


def authenticate(settings):
    password = keyring.get_password('sms_password', 'Administrator')
    if password is None:
        layout = [
            [sg.Text("No Administrator password found in keyring! \nEnter NEW Administrator password:")],
            [sg.InputText()],
            [sg.Button("Apply"), sg.Button("Exit")],
        ]
        window = sg.Window("NEW password", layout, finalize=True, modal=True)
        event, values = window.read()
        keyring.set_password('sms_password', 'Administrator', values[0])
        window.close()
        return True    
    else:
        auth = False
        layout = [
            [sg.Text("Enter Administrator password:")],
            [sg.InputText()],
            [sg.Button("Authenticate"), sg.Button("Exit")],
        ]
        window = sg.Window(
            "Authenticate as administrator", layout, finalize=True, modal=True
        )
        while True:
            event, values = window.read()

            if (values[0] != password) or event in (
                "Exit",
                sg.WIN_CLOSED,
            ):
                sg.popup(
                    "Error in Authentication, taking back to main menu.",
                    title="Authentication error",
                )
                auth = False
                break

            if values[0] == password:
                sg.popup(
                    "You can now access the settings menu.",
                    title="Authentication successful",
                )
                auth = True
                break
        window.close()
        return auth


def change_record(val, settings):
    name_email = settings.get("email", None)
    # print(str(val[0]).split()[-1])
    layout = [
        [sg.Text("Enter the new name: ")],
        [sg.InputText()],
        [sg.Text("Enter the new email:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Change record", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            del name_email[str(val[0]).split()[-1]]
            name_email[values[1]] = values[0]
            # name_email[:] = [values[0]+" - "+values[1] if x == val[0] else x for x in name_email]
            settings.set("email", name_email)
            sg.popup("Record changed successfully")
            break
    window.close()


def add_record(settings):
    name_email = settings.get("email", None)
    if name_email is None:
        name_email = {}
    # dict = settings.get("email", {"No record found" : "File doesn't exist"})
    layout = [        
        [sg.Text("Enter the new name: ")],
        [sg.InputText()],
        [sg.Text("Enter a new email:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Add record", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            name_email.update({values[1]: values[0]})
            # dict.update({values[1]: values[0]})
            settings.set("email", name_email)
            sg.popup("Record added successfully")
            break
    window.close()


def set_notification_limit(settings):
    notif_dict = settings.get('limit')
    # print(notif_dict)
    layout = [[sg.Text("Set notification limits.", font=('Montserrat', 10, 'bold'))]]
    for k, v in notif_dict.items():
        layout += [[sg.Text(k)], [sg.Slider(range=(1, 100), default_value=v, orientation='h', enable_events=True, key=k)]]
    layout += [[sg.Text("New values saved!", font=('Montserrat', 10, 'bold'), key='msg', visible=False)]]
    window = sg.Window("Set notification limits", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()
        if event in ("CPU", "Memory", "Storage", "Swap"):
            settings.set('limit', values)
            window.Element('msg').Update(visible = True)
        if event in ("Exit", sg.WIN_CLOSED):
            break
    window.close()

def delete_record(values, settings):
    name_email = settings.get("email", None)
    del name_email[str(values[0]).split()[-1]]
    settings.set("email", name_email)
    sg.popup("The selected record has been deleted.", title="Record deleted")

def change_password(settings):
    layout = [
        [sg.Text("Enter new password:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Change Password", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            keyring.set_password('sms_password', 'Administrator', values[0])
            sg.popup("Password changed successfully")
            break

    window.close()

# def parse_event(event, email, report_opt, email_opt, settings):

# def parse_values(values, auth, settings):

def email_report(email, resource):
    if email['id'] is None and email['password'] is None:
        layout = [
            [sg.Text("Enter the email: ")],
            [sg.InputText()],
            [sg.Text("Enter the password: ")],
            [sg.InputText(password_char='*')],
            [sg.Button("Save"), sg.Button("Exit")],
        ]
        window = sg.Window("Save details", layout, finalize=True, modal=True)
        while True:
            event, values = window.read()

            if event in ("Exit", sg.WIN_CLOSED):
                break

            elif event == "Save":
                email['id'] = values[0]
                email['password'] = values[1]
                break
        window.close()
    # sg.popup("")
    # for k,  v in email.items():
    #     print(k, v)
    
    # name_email = settings.get("email", None)
    # ems = ""
    # for k, v in name_email.items():
    #     ems += k+'\n'
    file = report.send_email(email['id'], email['password'], resource)
    sg.popup('Email sent from '+email['id']+' to the added emails with attachment '+file, title="Report sent successfully!")

def main():
    auth = False
    g = core.Get()

    sg.theme("SandyBeach")
    sg.set_options(font=('Montserrat', 10))

    settings = sg.UserSettings(filename="/home/$USER/.sms/settings.json")

    window = layout(g, settings)

    email = {
        'id': None,
        'password': None,
    }

    report_opt = {
        '-report-main-': 'Summary',
        '-report-cpu-' : 'CPU',
        '-report-mem-' : 'Memory',
        '-report-proc-': 'Process',
        '-report-storage-': 'Storage',
        '-report-net-' : 'Network',
        '-report-misc-': 'Miscellaneous'
    }
    email_opt = {
        '-email-main-': 'Summary',
        '-email-cpu-' : 'CPU',
        '-email-mem-' : 'Memory',
        '-email-proc-': 'Process',
        '-email-storage-': 'Storage',
        '-email-net-' : 'Network',
        '-email-misc-': 'Miscellaneous'
    }


    while True:
        event, values = window.read()
        # print(event, values)
        # parse_event(event, email, report_opt, email_opt, settingscd )
        # parse_values(values, auth, settings)
        if values[0] == "Settings Menu":
            if not auth:
                auth = authenticate(settings)
                if not auth:
                    window.Element("Main Menu").select()

        if event == sg.WIN_CLOSED:
            break
        if event == "Change password":
            sg.popup("Select an email from the list and try again!",
                        title="No email selected")
            change_password(settings)

        if event == "Add record":
            add_record(settings)
            n_e = [n+' - '+e for e, n in name_email.items()]
            window["-email-"].update(n_e)
            window.refresh()

        if event == "Change record" and not values['-email-']:
            sg.popup("Select an email from the list and try again!",
                        title="No email selected")
        elif event == "Change record" and values['-email-']:
            if values['-email-'][0] == "File doesn't exist - No record found":
                sg.popup("Add record and try again!", title="No record found")
            else:
                change_record(values['-email-'], settings)
                n_e = [n+' - '+e for e, n in name_email.items()]
                window["-email-"].update(n_e)
                window.refresh()

        if event == "Delete record" and not values['-email-']:
            sg.popup("Select an email from the list and try again!",
                        title="No email selected")
        elif event == "Delete record" and values['-email-']:
            if values['-email-'][0] == "File doesn't exist - No record found":
                sg.popup("Add record and try again!", title="No record found")
            else:
                delete_record(values['-email-'], settings)
                n_e = [n+' - '+e for e, n in name_email.items()]
                window["-email-"].update(n_e)
                window.refresh()
        
        if event == "Set notification limit":
            set_notification_limit(settings)


        if event in report_opt:
            file = report.down_report(report_opt[event])
            # print('report saved to file = ', file)
            sg.popup(report_opt[event] + " report saved to file " + file, title="Report generation successful!")
        elif event in email_opt:
            email_report(email, email_opt[event])

        # window['-update-'].update()
        # print(values['-email-'])
        # print(values[0])
    # window.refresh()
    window.close()

if __name__ == "__main__":
    main()
