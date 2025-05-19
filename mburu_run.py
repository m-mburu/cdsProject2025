
from main import run_cron_comparison, generate_sizes

sizes =generate_sizes(hpc=True)
repeat = 3
person_name = "Moses"
if __name__ == "__main__":
    run_cron_comparison(person_name, sizes, repeat)
    print("Run cron_comparison() to generate and save the results.")