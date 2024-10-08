book_initial = {}
book_additional = {}
total_expenses_by_person = {}

def add_initial_expenses():
    # Get all the dynamically created initial expense entries
    expense_entries = js.document.querySelectorAll('.expense-entry')
    for entry in expense_entries:
        name = entry.querySelector('.name').value
        amount = entry.querySelector('.amount').value
        if name and amount:
            try:
                amounts = list(map(int, amount.split()))
                total = sum(amounts)
                book_initial[name] = book_initial.get(name, 0) + total
                total_expenses_by_person[name] = total_expenses_by_person.get(name, 0) + total
            except ValueError:
                pass  # Ignore invalid input

def add_additional_expenses():
    # Get all the dynamically created additional expense entries
    additional_entries = js.document.querySelectorAll('.additional-expense-entry')
    for entry in additional_entries:
        anyother = entry.querySelector('.anyother').value
        amount = entry.querySelector('.extraAmount').value
        among = entry.querySelector('.among').value.split()
        if anyother and amount and among:
            try:
                # Calculate total additional amount
                total_amount = sum(map(int, amount.split()))
                num_people = len(among)
                if num_people > 0:
                    # Calculate contribution per person for additional expense
                    contribution = total_amount / num_people

                    # Update additional expenses book
                    book_additional[anyother] = book_additional.get(anyother, 0) + total_amount
                    total_expenses_by_person[anyother] = total_expenses_by_person.get(anyother, 0) + total_amount

                    # Distribute the amount among the specified people
                    for person in among:
                        # If a person appears in 'among' but not in initial expenses, add them with 0 initial expense
                        if person not in book_initial:
                            total_expenses_by_person[person] = 0

                        book_additional[person] = book_additional.get(person, 0) - contribution
                else:
                    print(f"Error: No one to split among for the additional expense '{anyother}'.")
            except ValueError:
                print(f"Error: Invalid amount '{amount}' for the additional expense '{anyother}'.")
                pass  # Ignore invalid input

def calculate_balances(book, total_spent):
    # Calculate the share per person
    number_of_people = len(book)
    if number_of_people > 0:
        share = total_spent / number_of_people
        for person in book:
            book[person] = round(book[person] - share, 2)

def calculate(event):
    global book_initial, book_additional, total_expenses_by_person
    book_initial = {}
    book_additional = {}
    total_expenses_by_person = {}

    # Step 1: Calculate initial expenses
    add_initial_expenses()

    # Step 2: Calculate additional expenses
    add_additional_expenses()

    if book_initial or book_additional:
        # Calculate the total expenses from both initial and additional
        total_spent_initial = sum(book_initial.values())
        total_spent_additional = sum(book_additional.values())

        # Calculate balance for initial expenses
        calculate_balances(book_initial, total_spent_initial)

        # Calculate balance for additional expenses
        calculate_balances(book_additional, total_spent_additional)

        # Clear existing result table
        result_div = js.document.getElementById('resultTable')
        result_div.innerHTML = ''

        # Create the table element
        table = js.document.createElement('table')
        table.setAttribute('border', '1')

        # Create table header
        header = js.document.createElement('tr')
        header_name = js.document.createElement('th')
        header_name.innerHTML = 'Name'
        header_total_balance = js.document.createElement('th')
        header_total_balance.innerHTML = 'Total Balance'
        #header_initial_expenses = js.document.createElement('th')
        #header_initial_expenses.innerHTML = 'Initial Spend'
        #header_additional_expenses = js.document.createElement('th')
        #header_additional_expenses.innerHTML = 'Additional Spend'
        header_total_expenses = js.document.createElement('th')
        header_total_expenses.innerHTML = 'Total Spend'
        header_total_expenditure = js.document.createElement('th')
        header_total_expenditure.innerHTML = 'Total Expenditure'
        header.appendChild(header_name)
        header.appendChild(header_total_balance)
        #header.appendChild(header_initial_expenses)
        #header.appendChild(header_additional_expenses)
        header.appendChild(header_total_expenses)
        header.appendChild(header_total_expenditure)
        table.appendChild(header)

        # Add rows for each person, their balance, initial spend, additional spend, total spend, and total expenditure
        for person in total_expenses_by_person:
            row = js.document.createElement('tr')

            cell_name = js.document.createElement('td')
            cell_name.innerHTML = person
            row.appendChild(cell_name)

            total_balance = book_initial.get(person, 0) + book_additional.get(person, 0)
            cell_total_balance = js.document.createElement('td')
            cell_total_balance.innerHTML = f"{total_balance:.2f}"  # Total balance
            row.appendChild(cell_total_balance)

            # Initial spend
            #cell_initial_expenses = js.document.createElement('td')
            #cell_initial_expenses.innerHTML = f"{book_initial.get(person, 0):.2f}"
            #row.appendChild(cell_initial_expenses)

            # Additional spend
            #cell_additional_expenses = js.document.createElement('td')
            #cell_additional_expenses.innerHTML = f"{book_additional.get(person, 0):.2f}"
            #row.appendChild(cell_additional_expenses)

            # Total spend (initial + additional)
            cell_total_expenses = js.document.createElement('td')
            cell_total_expenses.innerHTML = f"{total_expenses_by_person.get(person, 0):.2f}"
            row.appendChild(cell_total_expenses)

            # Calculate Total Expenditure = Total Spend - Total Balance
            total_expenditure = total_expenses_by_person.get(person, 0) - total_balance
            cell_total_expenditure = js.document.createElement('td')
            cell_total_expenditure.innerHTML = f"{total_expenditure:.2f}"  # Total Expenditure
            row.appendChild(cell_total_expenditure)

            table.appendChild(row)

        # Add row for total spend
        total_row = js.document.createElement('tr')
        total_cell_name = js.document.createElement('td')
        total_cell_name.innerHTML = 'Total Spend'
        total_row.appendChild(total_cell_name)

        total_cell_total_balance = js.document.createElement('td')
        total_cell_total_balance.innerHTML = ''  # No balance for total spend row
        total_row.appendChild(total_cell_total_balance)

        total_cell_total_expenses = js.document.createElement('td')
        total_cell_total_expenses.innerHTML = f"{sum(total_expenses_by_person.values()):.2f}"  # Total spend
        total_row.appendChild(total_cell_total_expenses)

        total_cell_total_expenditure = js.document.createElement('td')
        total_cell_total_expenditure.innerHTML = f"{sum(total_expenses_by_person.values()):.2f}"  # total expenditure
        total_row.appendChild(total_cell_total_expenditure)

        table.appendChild(total_row)

        result_div.appendChild(table)
    else:
        js.document.getElementById('resultTable').innerHTML = "No valid entries found."

# Bind the calculate button to the Python calculate function
Element('calculateBtn').element.onclick = calculate
