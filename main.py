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
    search_terms = list(search_terms.split('\n'))

scriptusage="Usage: python3 main.py --name username/organizationname [Optional: --mode orgs[organizations]/users[users] , --debug, --help]"

if "--help" in sys.argv:
    print(scriptusage)
    sys.exit()


# if len(sys.argv)<2:
#     print(scriptusage)
#     sys.exit()

# if "--mode" in sys.argv:
#     if sys.argv[sys.argv.index("--mode")+1] == "orgs":
#         type="orgs"
#     elif sys.argv[sys.argv.index("--mode")+1] == "users":
#         pass
#     else:
#         print(scriptusage)
# else:
#     type="users"

# if "--debug" in sys.argv:
#     debug_mode=True
# else:
#     debug_mode=False

# try:
#     github_username = sys.argv[sys.argv.index("--name")+1]
# except:
#     print(scriptusage)
type="users"
github_username = "acikkaynak"
debug_mode=True

def apiSign():
    #API limit bypass
    token=base64.b64encode(b'myclientid:SECRETKEY').decode()
    apiLimitBypass={"Authorization": f"Basic {token}", "Accept": "application/vnd.github.v3.text-match+json"} 
    return apiLimitBypass

# Select mail from raw text
def keysearch(responsein):
    for line in responsein.split("\n"):
        for keyword in search_terms:
            if keyword in line:
                print("\033[93m"+line,responsein.split("\n")[responsein.split("\n").index(line)+1]+"\033[0m"); logging = open("log.txt", "a"); logging.write("\033[93m"+line+responsein.split("\n")[responsein.split("\n").index(line)+1]+"\033[0m\n"); logging.close()
    return None


def main():

    try:
        table = PrettyTable()
        table.field_names = ["Found Repo","Found Commit SHA", "Found Leak"]
        found=[]

        # Get Repositories
        urlForGetReposRaw = f"https://api.github.com/{type}/{github_username}/repos"
        print(urlForGetReposRaw)
        responseForRepos = requests.get(urlForGetReposRaw, headers=apiSign()).text
        reporaw = json.loads(responseForRepos)
        for repository in reporaw:
            repoName=(repository["name"])
            if repoName in repolist:

                f = open("scanned.data", "r+")                
                saved_session = f.readlines()
                f.write(str(repoName)+"\n")


                if debug_mode:print("Searching in "+str(repoName)); logging = open("log.txt", "a"); logging.write("Searching in "+str(repoName)+"\n"); logging.close()
                urlforgetcommitsraw=f"https://api.github.com/repos/{github_username}/{repoName}/commits"
                responseforcommits = requests.get(urlforgetcommitsraw, headers=apiSign()).text
                commitsraw = json.loads(responseforcommits)

                for commits in commitsraw:
                        
                    temporary_=[]
                    temporary_.append(commits["sha"])
                    
                    
                    if debug_mode:print("Commit:"+str(commits["sha"]));logging = open("log.txt", "a"); logging.write("Commit:"+str(commits["sha"])+"\n"); logging.close()

                    for commitsha in temporary_:
                        if commitsha+"\n" in saved_session:
                            print("Already Scanned")
                            break

                        response = requests.get(f"https://github.com/{github_username}/{repoName}/commit/{commitsha}.patch").text
                        clean = keysearch(response)
                        f.writelines(str(commitsha)+"\n")
                        if clean != None:
                            if debug_mode: print("\033[93m"+str(clean)+"\033[0m")
                            table.add_row([repoName, commitsha, clean])
                            found.append(clean)
                                                        

        print(table)
        f.close()

    except KeyboardInterrupt:
        print("Ctrl+C pressed")
        f.close()
        sys.exit()


if __name__ == "__main__":
    main()