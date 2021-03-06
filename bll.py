from dal import connect


@connect
def list_name_of_mentors(cursor):
    """
    returns the 2 name columns of the mentors table.
    :return: first_name, last_name
    """
    cursor.execute("""SELECT first_name, last_name FROM mentors ORDER BY first_name ASC;""")
    rows = cursor.fetchall()
    return rows


@connect
def get_mentors_by_city(cursor, city):
    """
    returns the nick_name-s of all mentors working at a specific city.
    :param city: name of city
    :return: nick_name
    """
    cursor.execute("""SELECT nick_name FROM mentors WHERE city = '{}';""".format(str.capitalize(city)))
    rows = cursor.fetchall()
    return rows


@connect
def get_applicant_info(cursor, first_name):
    """
    returns the full_name-s and phone_number-s of an applicant by their first_name
    :param first_name: first name of an applicant
    :return: full_name, phone_number
    """
    cursor.execute("""SELECT first_name, last_name, phone_number
    FROM applicants WHERE first_name = '{}';""".format(first_name))
    rows = cursor.fetchall()
    return rows


@connect
def get_applicant_info_by_emai(cursor ,email):
    """
    returns the full_name-s and phone_number-s of an applicant by their university.
    :param email: name of university
    :return: full_name, phone_number
    """
    cursor.execute("""SELECT first_name, last_name, phone_number
    FROM applicants WHERE email LIKE '%{}%';""".format(str.lower(email)))
    rows = cursor.fetchall()
    return rows

@connect
def add_new_applicant(cursor, applicant):
    """
    returns the whole row of the inserted applicant
    :param applicant: list of attributes
    :return: id, first_name, last_name, phone_number, email, application_code
    """
    cursor.execute("""INSERT INTO applicants (first_name, last_name, phone_number, email, application_code) 
    VALUES('{}', '{}', '{}', '{}', '{}');""".format(applicant[0], applicant[1], applicant[2], applicant[3], applicant[4]))

    cursor.execute("""SELECT * FROM applicants WHERE application_code = {};""".format(applicant[4]))
    rows = cursor.fetchall()
    return rows


@connect
def update_applicant_phone_number(cursor, applicant_name, phone_number):
    """
    returns the phone_number of the current applicant
    :param applicant_name: list of applicant first and last name
    :param phone_number: phone number
    :return: phone_number
    """
    cursor.execute("""UPDATE applicants set phone_number = '{2}'
    WHERE first_name = '{0}' and last_name = '{1}';""".format(applicant_name[0], applicant_name[1], phone_number))
    cursor.execute("""SELECT phone_number FROM applicants
    WHERE first_name = '{}' and last_name = '{}';""".format(applicant_name[0], applicant_name[1]))
    rows = cursor.fetchall()
    return rows


@connect
def remove_applicant(cursor, domain):
    cursor.execute("""SELECT * FROM applicants WHERE email LIKE '%{}';""".format(domain))
    try:
        email = cursor.fetchall()[0]
    except IndexError:
        return 'There is no applicant with emails for this domain'
    cursor.execute("""DELETE FROM applicants WHERE email LIKE '%{}';""".format(domain))
    return 'Applicant(s) has been removed from the database'


@connect
def get_custom_attributes(cursor, table, attributes=''):
    """
    returns the given attributes
    :param table: db_table
    :param attributes: set of attributes
    :return: give_attributes
    """
    cursor.execute("""SELECT {} FROM {};""".format(attributes, table))
    rows = cursor.fetchall()
    return rows


@connect
def get_mentors_and_school(cursor):
    cursor.execute("""SELECT  concat(mentors.first_name, ' ', mentors.last_name), schools.name, schools.country \
    FROM mentors INNER JOIN schools ON mentors.city = schools.city ORDER BY mentors.id ASC;""")
    rows = cursor.fetchall()
    return rows


@connect
def get_mentors_and_all_school(cursor):
    cursor.execute("""SELECT  concat(mentors.first_name, ' ', mentors.last_name), schools.name, schools.country \
    FROM mentors RIGHT JOIN schools ON mentors.city = schools.city ORDER BY mentors.id ASC;""")
    rows = cursor.fetchall()
    return rows


@connect
def mentors_by_country(cursor):
    cursor.execute("""SELECT schools.country, count(mentors.city) AS count \
     FROM schools INNER JOIN mentors ON schools.city = mentors.city GROUP BY country ORDER BY schools.country;""")
    rows = cursor.fetchall()
    return rows


@connect
def get_contact_mentors(cursor):
    cursor.execute("""SELECT schools.name, concat(mentors.first_name, ' ', mentors.last_name) \
    FROM schools INNER JOIN mentors ON schools.contact_person = mentors.id ORDER BY schools.name ASC;""")
    rows = cursor.fetchall()
    return rows


@connect
def get_applicants(cursor):
    cursor.execute("""SELECT applicants.first_name, applicants.application_code, applicants_mentors.creation_date \
    FROM applicants INNER JOIN applicants_mentors ON applicants_mentors.applicant_id = applicants.id \
     WHERE applicants_mentors.creation_date > '2016-01-01' ORDER BY creation_date DESC;""")
    rows = cursor.fetchall()
    return rows


@connect
def get_applicants_and_mentors(cursor):
    cursor.execute("""SELECT applicants.first_name, applicants.application_code, \
     concat(mentors.first_name,  ' ', mentors.last_name) FROM applicants \
      LEFT JOIN applicants_mentors ON applicants_mentors.applicant_id = applicants.id \
      LEFT JOIN mentors ON applicants_mentors.mentor_id = mentors.id ORDER BY applicants.id ASC;""")
    rows = cursor.fetchall()
    return rows
