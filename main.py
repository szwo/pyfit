import ioService
import restService

current_profile = {}


# Current Profile Global Var Helpers

def update_day():
    global current_profile
    current_profile['day'] = current_profile['day'] + 1
    save_profile()


def update_last_muscle_group(last_muscle_group):
    global current_profile
    current_profile['lastMuscleGroup'] = last_muscle_group
    save_profile()


def save_profile():
    ioService.save_file('profile', current_profile)


def create_new_profile():
    global current_profile
    current_profile = {'day': 1, 'lastMuscleGroup': ''}
    save_profile()


# General Functions

def request_input(prompt):
    value = input(prompt)
    return value


def request_workout(category, category_id):
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
        print('Exercise found!')
        update_last_muscle_group(category)
        update_day()
    else:
        print('\nPlease enter in a valid exercise!')
        request_workout(category, category_id)

    # TODO: Next, we will ask them if they need more information for the workout


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
        request_workout(requested_category, categories[requested_category.lower()])
    else:
        print('\nPlease enter in a valid muscle group:')
        request_category()


def determine_day_in_challenge():
    if ioService.does_file_exist('profile'):
        global current_profile
        current_profile = ioService.open_file('profile')
        print('Welcome back to the challenge! You are on Day', current_profile['day'])
        if current_profile['lastMuscleGroup']:
            print('Your last exercised muscle group:', current_profile['lastMuscleGroup'], '\n')
    else:
        print('Are you ready to start the challenge? Welcome to Day 1!')
        create_new_profile()


# Main Function

def main():
    print('Welcome to PyFit, your 90-day challenge assistant!\n')
    determine_day_in_challenge()
    request_category()


main()
