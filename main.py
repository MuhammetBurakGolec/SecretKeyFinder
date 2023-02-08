import requests
from prettytable import PrettyTable
import base64
import json
import sys
import progress

with open ('itdeprem.data', 'r') as f:
    data = f.read()
    repolist = list(data.split('\n'))
with open ('searchterms.data', 'r') as f:
    search_terms = f.read()
    search_terms = list(data.split('\n'))

scriptusage="Usage: python3 main.py --name username/organizationname [Optional: --mode orgs[organizations]/users[users] , --debug, --help]"

if "--help" in sys.argv:
    print(scriptusage)
    sys.exit()

#if len(sys.argv)<3:
if len(sys.argv)<2:
    print(scriptusage)
    sys.exit()

if "--mode" in sys.argv:
    if sys.argv[sys.argv.index("--mode")+1] == "orgs":
        type="orgs"
    elif sys.argv[sys.argv.index("--mode")+1] == "users":
        pass
    else:
        print(scriptusage)
else:
    type="users"

if "--debug" in sys.argv:
    debug_mode=True
else:
    debug_mode=False

try:
    #github_username = sys.argv[sys.argv.index("--name")+1]
    github_username = "acikkaynak"
except:
    print(scriptusage)

def apiSign():
    #API limit bypass
    token=base64.b64encode(b'myclientid:KEY').decode()
    apiLimitBypass={"Authorization": f"Basic {token}", "Accept": "application/vnd.github.v3.text-match+json"} 
    return apiLimitBypass

# Select mail from raw text
def keysearch(responsein):
    newlist=[]
    for line in responsein.split("\n"):
        for keyword in search_terms:
            if keyword in line:
                print("\033[93m"+line,responsein.split("\n")[responsein.split("\n").index(line)+1]+" found.\033[0m")
    return None


def main():

    # Get Repositories
    urlForGetReposRaw = f"https://api.github.com/{type}/{github_username}/repos"
    responseForRepos = requests.get(urlForGetReposRaw, headers=apiSign).text
    reporaw = json.loads(responseForRepos)

    for repository in reporaw:
        repoName=(repository["name"])
        if repoName in repolist:
            if debug_mode:print("Searching in "+str(repoName))
            
            urlforgetcommitsraw=f"https://api.github.com/repos/{github_username}/{repoName}/commits"
            responseforcommits = requests.get(urlforgetcommitsraw, headers=apiSign).text
            commitsraw = json.loads(responseforcommits)
            
            for commits in commitsraw:
                temporary_=[]
                temporary_.append(commits["sha"])
                
                #Debug
                if debug_mode:print("Commit:"+str(commits["sha"]))

                for commitsha in temporary_:
                    response = requests.get(f"https://github.com/{github_username}/{repoName}/commit/{commitsha}.patch").text
                    clean = keysearch(response)
                    if clean != None:
                        if debug_mode: print("\033[93m"+str(clean)+" found.\033[0m")
                        table.add_row([repoName, commitsha, clean])
                        found.append(clean)

print(table)


if __name__ == "__main__":
    main()