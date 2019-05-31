class Job:
    def __init__(self, Id, weight, length):
        self.Id = Id
        self.weight = weight
        self.length = length
        self.ratio = self.weight / self.length

    def __gt__(self, job):
        if self.ratio == job.ratio:
            return self.weight > job.weight
        else:
            return self.ratio > job.ratio
    
    def __lt__(self, job):
        if self.ratio == job.ratio:
            return self.weight < job.weight
        else:
            return self.ratio < job.ratio

def read_txt(path):
    """
    Read the txt file and return a graph.
    """

    jobs = []
    with open(path) as file:
        lines = file.readlines()

        Id = 1
        for line in lines[1:]:
            weight, length = line.split(' ')
            weight, length = int(weight), int(length)
            jobs.append(Job(Id, weight, length))
            Id += 1

    return jobs

def schedule(jobs):
    """
    Schedule the jobs with greedy algorithm
    """

    jobs = sorted(jobs, reverse=True)
    acc = 0
    weighted = 0
    for job in jobs:
        acc += job.length
        weighted += job.weight * acc
    return weighted


if __name__ == "__main__":
    jobs = read_txt('jobs.txt')
    jobs = sorted(jobs)
    print(schedule(jobs))
    # output: 67311454237