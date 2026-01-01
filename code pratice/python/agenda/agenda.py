#!/usr/bin/env python3

import time
import os 

# Global dictionary to store contacts
CONTACTS = dict()


def show_contacts():
    """Iterates through the contacts and displays them."""
    if CONTACTS: 
        for contact in CONTACTS: 
            search_contact(contact)
    else: 
        print("\nContact list is empty!") 


def search_contact(name):
    """Searches and prints details of a specific contact."""
    try: 
        print(f'\nName: {name}')
        print(f"Phone: {CONTACTS[name]['phone']}")
        print(f"E-mail: {CONTACTS[name]['email']}")
        print(f"Address: {CONTACTS[name]['address']}")
        print('\n|>------------------<|') 
    
    except KeyError:
        os.system('clear') 
        print('''
        o----------------------------------------------------------------------o
        |      ⚠️                                                              |
        |      Oops...! An error occurred :/                                   |
        |      Please, provide a contact that exists in the list! :)           |
        |                                                                      |     
        o----------------------------------------------------------------------o
              ''') 
    

def get_contact_details():
    """Prompts the user for contact information."""
    phone = input('Phone: ')
    email = input('Contact E-mail: ')
    address = input('Address: ')

    return phone, email, address


def add_edit_contact(name, phone, email, address):
    """Adds a new contact or updates an existing one."""
    CONTACTS[name] = {
        'phone': phone,
        'email': email,
        'address': address,        
    } 
    save_data()
    print(f'\n> Contact "{name}" successfully added/updated! :)') 


def delete_contact(name):
    """Removes a contact from the dictionary."""
    try:
        del CONTACTS[name]
        save_data()
        print(f'\nContact "{name}" successfully deleted!')

    except KeyError:
         print('''
        o---------------------------------------------------------------o
        |      ⚠️                                                       |
        |      Oops...! An error occurred :/                            |
        |      Please, choose an existing contact!                      |
        |                                                               |
        o---------------------------------------------------------------o
              ''') 


def export_contacts(file_name):
    """Exports the contact list to a CSV file."""
    try:
        with open(file_name, 'w') as file:
            for name in CONTACTS:
                file.write(f"{name};{CONTACTS[name]['phone']};{CONTACTS[name]['email']};{CONTACTS[name]['address']}\n")

        os.system('clear')
        print(f'>> Contacts successfully exported to {file_name} <<')

    except Exception:
        print('>> An error occurred while exporting contacts..! <<') 


def import_contacts(file_name):
    """Imports contacts from a CSV file."""
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                details = line.strip().split(';')
                if len(details) == 4:
                    add_edit_contact(details[0], details[1], details[2], details[3])

    except FileNotFoundError:
        print('\n>> File not found! <<') 

    except Exception as error:
        print('An unexpected error occurred!') 
        print(error)


def save_data():
    """Auto-saves the current state to the database file."""
    export_contacts('database.csv')


def load_data():
    """Loads contacts from the database file on startup."""
    try:
        if not os.path.exists('database.csv'):
            return

        with open('database.csv', 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                details = line.strip().split(';')
                if len(details) == 4:
                    CONTACTS[details[0]] = {
                        'phone': details[1], 
                        'email': details[2],
                        'address': details[3],
                    }
        print(f'\n {len(CONTACTS)} contacts loaded...')
    except FileNotFoundError:
        print('Database file not found, starting fresh.') 

    except Exception as error:
        print('An unexpected error occurred while loading data!') 
        print(error)


def print_menu():
    """Displays the main menu options."""
    print('\n--- MAIN MENU ---') 
    print('\n1 - Show all contacts')
    print('2 - Search contact')
    print('3 - Add new contact')
    print('4 - Edit contact')
    print('5 - Delete contact')
    print('6 - Export contacts to CSV')
    print('7 - Import contacts from CSV')
    print('0 - Exit program\n')


def get_option():
    """Handles user input for menu selection."""
    valid_options = ['0', '1', '2', '3', '4', '5', '6', '7']
    option = input('\nChoose an option (number): ')

    if option in valid_options:
        return option
    
    else: 
        print('''
        o---------------------------------------------------------------o
        |      ⚠️                                                       |
        |      Oops...! An error occurred :/                            |
        |      Please, choose a valid option (from 0 to 7)! :)          |
        |                                                               |
        o---------------------------------------------------------------o
              ''') 


# Initializing the application
load_data()

while True:
    print_menu()

    match get_option():
        case '0':
            print("Exiting application... Goodbye!")
            break
        
        case '1':
            os.system('clear')
            show_contacts()
            time.sleep(2)

        case '2': 
            print('\n > Please enter the contact name you wish to find:\n')
            name = input('Name: ')
            search_contact(name)

        case '3':
            print('\nAdding a new contact!') 
            print('\n > We will need some information...\n')

            name = input('Contact Name: ')

            if name in CONTACTS:
                os.system('clear') 
                print('\n >> Oops... This contact already exists! <<') 
                time.sleep(2)
                continue

            phone, email, address = get_contact_details()
            add_edit_contact(name, phone, email, address)
             
            time.sleep(2)
            os.system('clear')

        case '4':
            print('\n > We will need some information...\n')
            name = input('Contact Name to edit: ') 

            if name in CONTACTS: 
                print('\nEditing contact details!') 
                phone, email, address = get_contact_details()
                add_edit_contact(name, phone, email, address)
                time.sleep(2)
                os.system('clear')
            else:
                print('\nThis contact does not exist!') 
                time.sleep(2)
                os.system('clear')

        case '5':
            name = input('\nPlease enter the name of the contact you want to DELETE: ')
            delete_contact(name)

        case '6':
            file_name = input('\nEnter the filename for export (e.g., backup.csv): ')
            export_contacts(file_name)

        case '7':
            file_name = input('\nEnter the filename to import from: ')
            import_contacts(file_name)