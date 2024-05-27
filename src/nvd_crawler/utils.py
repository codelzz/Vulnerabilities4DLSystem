import json
import pandas as pd


class JSONParser:
    def __init__(self, raw_dir, distilled_dir):
        self.json_dir = raw_dir
        self.csv_dir = distilled_dir

    def parse(self, framework):
        json_dir = self.json_dir + f'nvd_{framework}.json'
        csv_dir  = self.csv_dir  + f'nvd_{framework}.csv'

        with open(json_dir, 'r') as f:
            temp = json.loads(f.read())
            with open(csv_dir, "wb") as empty_csv:
                pass

            accessComplexity = []
            authentication = []
            availability = []
            confidentiality = []
            CWE = []
            CVEID = []
            description = []
            score = []
            integrity = []
            commitsList = []

            CVSS3List = ['attackVector', 'attackComplexity', 'privilegesRequired', 'userInteraction', 'scope',
                         'confidentialityImpact', 'integrityImpact', 'availabilityImpact', 'baseScore', 'baseSeverity']
            CVSS3Data = []
            for x in range(len(CVSS3List)):
                CVSS3Data.append([])
            tempArray = temp['result']['CVE_Items']
            for temp in tempArray:
                # Extracting CVSS2 metric data and CVE relative infor
                try:
                    CVEID.append(temp['cve']['CVE_data_meta']['ID'])
                except Exception as e:
                    print("[Error] no CVEID, previous ID is " + CVEID[-1])
                    print(e)
                    CVEID.append("")

                try:
                    accessComplexity.append(temp['impact']['baseMetricV2']['cvssV2']['accessComplexity'])
                except Exception as e:
                    accessComplexity.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                try:
                    authentication.append(temp['impact']['baseMetricV2']['cvssV2']['authentication'])
                except Exception as e:
                    authentication.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                try:
                    availability.append(temp['impact']['baseMetricV2']['cvssV2']['availabilityImpact'])
                except Exception as e:
                    availability.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                try:
                    confidentiality.append(temp['impact']['baseMetricV2']['cvssV2']['confidentialityImpact'])
                except Exception as e:
                    confidentiality.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                try:
                    CWE.append(temp['cve']['problemtype']['problemtype_data'][0]['description'][0]['value'])
                except Exception as e:
                    CWE.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                try:
                    description.append(temp['cve']['description']['description_data'][0]['value'])
                except Exception as e:
                    description.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                try:
                    score.append(temp['impact']['baseMetricV2']['cvssV2']['baseScore'])
                except Exception as e:
                    score.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                try:
                    integrity.append(temp['impact']['baseMetricV2']['cvssV2']['integrityImpact'])
                except Exception as e:
                    integrity.append("")
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)

                # Extracting commit ID
                links = temp['cve']['references']['reference_data']
                commits = ""
                for link in links:
                    link = link['url']
                    if "commit/" in link:
                        commits += link.split('commit/')[1] + ", "
                    elif "commits/" in link:
                        commits += link.split('commits/')[1] + ", "
                commits = commits[:-2]
                commitsList.append(commits)

                # Extracting CVSS3 metric data
                try:
                    tempCVSS3 = temp['impact']['baseMetricV3']['cvssV3']
                    for x in range(len(CVSS3List)):
                        try:
                            CVSS3Data[x].append(tempCVSS3[CVSS3List[x]])
                        except Exception as e:
                            CVSS3Data[x].append("")
                            print("[Error] CVE: " + CVEID[-1] + " %s" % e)
                except Exception as e:
                    print("[Error] CVE: " + CVEID[-1] + " %s" % e)
                    for x in range(len(CVSS3List)):
                            CVSS3Data[x].append('')

            # Store the extracted data as dataframe
            dataframe = pd.DataFrame(
                {'commit hash': commitsList, 'CWE ID': CWE, 'CVE ID': CVEID,
                 'CVSS2 Access Complexity': accessComplexity,
                 'CVSS2 Authentication Required': authentication,
                 'CVSS2 Availability Impact': availability, 'CVSS2 Confidentiality Impact': confidentiality,
                 'CVSS2 Score': score, 'CVSS2 Integrity Impact': integrity})
            for x in range(len(CVSS3List)):
                dataframe["CVSS3" + CVSS3List[x]] = CVSS3Data[x]

            dataframe['Description'] = description

            # Parse the dataframe to csv file
            dataframe.to_csv(csv_dir, index=False, sep=',')
