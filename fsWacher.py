#__authoer = "RaviTeja Mandapati"
#__version = "1.0.0 - RC1"
#__datetime = "2018-05-18 00:48:56"
#
import yaml
import argparse
import sys
import datetime

try:
    ymlfile = 'config.yml'
    ymlstream = open(ymlfile,'r').read()
except:
    print("Please check the config.yml file.")
    sys.exit(1)

def push_to_config():
    pass

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-li", "--list", help="Subscription Status (True/False)", type=bool, default=False, choices=[True, False])
parser.add_argument("-s", "--subscription", help="Subscription Status (True/False)", type=str, default="True", choices=['True', 'False'])
parser.add_argument("-l", "--location", help="Location Of The Subscribed Mount Path", type=str)
parser.add_argument("-m", "--mount", help="Linux Mount Path", type=str)
parser.add_argument("-w", "--warning", help="Warning Threshold (Recomended between 85 to 90)", type=int, default=85)
parser.add_argument("-e", "--error", help="Error Threshold (Recomended between 90 to 95)", type=int, default=95)
parser.add_argument("-n", "--notification", help="Notification email addressess ( Use comma as a separator )", type=str, default="xhdstorageteam@xilinx.com")
args = parser.parse_args()

if args.list:
    print("Monitoring Enabled Mounts & Their Respective Details.")
    for watcher in yaml.load(ymlstream)["watchers"]:
        print(watcher)
    sys.exit(0)
else:
    if args.location and args.mount:
        print(yaml.load(ymlstream)["banner"])
        if (args.location in yaml.load(ymlstream)["locations"]):
            configResult = yaml.load(ymlstream)
            if args.subscription == "True" or args.subscription == "true" or args.subscription == "False" or args.subscription == "false":
                if args.subscription == "True" or args.subscription == "true":
                    newRecord = {
                        "location": args.location,
                        "mount": args.mount,
                        "warning": args.warning,
                        "error": args.error,
                        "emails": args.notification,
                        "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if ("watchers" in yaml.load(ymlstream)):
                        watcherList = yaml.load(ymlstream)["watchers"]
                        for watcher in watcherList:
                            if watcher["location"] == args.location and watcher["mount"] == args.mount:
                                print("Duplicate record found. Please verify the values once again.")
                                sys.exit(1)
                        watcherList.append(newRecord)
                        configResult["watchers"] = watcherList
                    else:
                        configResult["watchers"] = [ newRecord ]
                    print("Mount was successfully added to wacher list.")
                else:
                    if ("watchers" in yaml.load(ymlstream)):
                        watcherList = yaml.load(ymlstream)["watchers"]
                        for watcher in yaml.load(ymlstream)["watchers"]:
                            if watcher["location"] == args.location and watcher["mount"] == args.mount:
                                del watcherList[watcherList.index(watcher)]
                        configResult["watchers"] = watcherList
                        print("Mount was successfully removed from wacher list.")
                    else:
                        print("No wachers found to remove from configuration")
            else:
                parser.print_help()
                sys.exit(1)
            with open('config.yml', 'w') as yaml_file:
                yaml.dump(configResult, yaml_file, default_flow_style=False)
        else:
            print("Please select valied site.")
    else:
        parser.print_help()

# END
