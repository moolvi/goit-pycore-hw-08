import pickle
from classes import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return f'{error}'
        except IndexError as error:
            return f'{error}'
        except KeyError as error:
            return f'{error}'
        except Exception as error:
            return f'{error}'
        finally:
            pass
    return inner


@input_error
def parse_input(user_input):
# Function return a list with arguments or a error code.
    
    if user_input and user_input.count(' ') == 0:
        cmd = user_input
    elif user_input.count(' ') > 0:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
    else:
        raise ValueError('Error: Input is empty\n')
    
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    message = ""
    if len(args) > 0:
        name, *args = args
        phone = None
        if args and len(args) > 0:
            phone, *_ = args
        record = book.find(name)
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added.\n"
        else:
            message = "The contact exists in the book phone.\n"
        if phone:
            record.add_phone(phone)
            message = f"{message}Phone added.\n"
    else:
        raise ValueError('Error: Contact name must not be empty.')
    
    return message


@input_error
def change_contact(args, book: AddressBook):
# Updates an existing contact or adds a new one.
    if len(args) > 0:
        name, *args = args
        phone = None
        new_phone = None
        record = book.find(name)
        if record:
            if len(args) > 1:
                phone, new_phone, *_ = args
                record.edit_phone(phone, new_phone)
                return 'Phone updated.'
            elif len(args) > 0:
                phone, *_ = args
                record.add_phone(phone)
                return 'Phone added.'
            else:
                raise ValueError('Warning: New phone number not specified.')
        else:
            return add_contact([name, *args], book)
    else:
        raise ValueError ('Warning: Contact name is empty.')


@input_error
def show_phone(name: str, book: AddressBook):
    if isinstance(name, str) and name and (name in book.data):
        record = book.data[name]
        if isinstance(record, Record):
            return (f'{name}: {', '.join(phone.value for phone in record.phones)}\n')
        else:
            raise TypeError("Error: The resulting contact format does not match the expected format.n")
    else:
        raise ValueError("Warning: No contact.\n")


@input_error
def show_all(book: AddressBook):
    if isinstance(book, AddressBook) and book and book.data:
        return ''.join(str(value) for value in book.data.values())
    else:
        raise TypeError("Error: The adressbook doesn't fit the format.\n")


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) > 1:
        name, birthday = args
        if not(isinstance(name, str) and name):
            raise TypeError("Warning: Contact name must not be empty.\n")
        if isinstance(book, AddressBook) and book and book.data and isinstance(book.data[name], Record):
            book.data[name].add_birthday(birthday)
        else:
            raise TypeError("Error: The adressbook doesn't fit the format.\n")
    else:
        raise TypeError("Warning: Missing contact name or date of birthday.\n")


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) > 1:
        name, *_ = args
        if not(isinstance(name, str) and name):
            raise TypeError("Warning: Contact name must not be empty.\n")
        if isinstance(book, AddressBook) and book and book.data and isinstance(book.data[name], Record):
            return book.data[name].birthday
        else:
            raise TypeError("Error: The adressbook doesn't fit the format.\n")
    else:
        raise TypeError("Warning: Missing contact name or date of birthday.\n")


@input_error
def show_birthdays(book: AddressBook):
    result = ''
    if isinstance(book, AddressBook):
        for item in book.get_upcoming_birthdays():
            result = result.join(f'{key}: {item[key]}' for key in item)
        return result
    raise TypeError("Error: The adressbook doesn't fit the format.\n")


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()

    #print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if (" " not in user_input):
            user_input = f'{user_input} '
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args[0], book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            add_birthday(args, book)

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_birthdays(book))
        else:
            print("Invalid command.")
    
    save_data(book)

if __name__ == "__main__":
    main()