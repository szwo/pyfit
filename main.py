import ioService
import restService

current_profile = {}


# Current Profile Global Var Helpers

def update_weight():
    global current_profile
    current_profile['currentWeight'] = request_input('Let\'s update your profile. What is your current weight?: ')
    # Do not save until they have completed the workout


def update_day():
    global current_profile
    current_profile['day'] = current_profile['day'] + 1
    # Do not save until they have completed the workout


def update_last_muscle_group(last_muscle_group):
    global current_profile
    current_profile['lastMuscleGroup'] = last_muscle_group
    # Do not save until they have completed the workout


def open_profile():
    global current_profile
    current_profile = ioService.open_file('profile')


def save_profile():
    ioService.save_file('profile', current_profile)


def create_new_profile():
    global current_profile

    print('Before we start, PyFit needs some information from you... \n')
    current_weight = request_input('What is your current weight (in lbs)? ')
    print('')
    target_weight = request_input('What is your target weight (in lbs)? ')
    print('')

    current_profile = {'day': 1, 'lastMuscleGroup': '', 'currentWeight': current_weight, 'targetWeight': target_weight}
    save_profile()


# General Functions

def request_input(prompt):
    value = input(prompt)
    return value


def request_exercise_status():
    selection = request_input('Are you finished this exercise? (y/n): ')
    if selection.lower() == 'y':
        print('Woohoo! Congrats on making it through another day in the challenge!')
        save_profile()
    elif selection.lower() == 'n':
        print('Keep going!')
        print()
        request_exercise_status()
    else:
        print()
        request_exercise_status()


def request_workout_options(exercise):
    print('Great choice! Here is a quick description of the workout:')
    print(exercise['description'])
    request_exercise_status()


def request_workout(category_id):
    print('Here are some workouts you can choose from, select one: \n')
    raw_exercises = restService.get_exercises_by_category(category_id)['results']
    exercises = {}
    for i in range(len(raw_exercises)):
        exercise = raw_exercises[i]['name']
        key = exercise.lower()
        value = raw_exercises[i]
        exercises[key] = value
        print(exercise)

    requested_exercise = request_input('\nYour selection: ')
    if requested_exercise.lower() in exercises:
        request_workout_options(exercises[requested_exercise.lower()])
    else:
        print('\nPlease enter in a valid exercise!')
        request_workout(category_id)


def request_category():
    print('For today\'s workout, please select a muscle group:')
    raw_categories = restService.get_exercise_categories()
    categories = {}
    for i in range(len(raw_categories)):
        category = raw_categories[i]['name']
        key = category.lower()
        value = raw_categories[i]['id']
        categories[key] = value
        print(category)

    requested_category = request_input('\nYour selection: ')
    if requested_category.lower() in categories:
        update_last_muscle_group(requested_category)
        request_workout(categories[requested_category.lower()])
    else:
        print('\nPlease enter in a valid muscle group:')
        request_category()


def determine_day_in_challenge():
    if ioService.does_file_exist('profile'):
        open_profile()
        print('Welcome back to the challenge! You are on Day', current_profile['day'])
        print('Your target weight is:', current_profile['targetWeight'], 'lbs')
        if current_profile['lastMuscleGroup']:
            print('Your last exercised muscle group:', current_profile['lastMuscleGroup'], '\n')
        update_day()
    else:
        print('Are you ready to start the challenge? Welcome to Day 1!')
        create_new_profile()


# Main Function

def main():
    print('Welcome to PyFit, your 90-day challenge assistant!\n')
    determine_day_in_challenge()
    request_category()


main()
