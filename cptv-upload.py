from deviceapi import DeviceAPI

import argparse
import os
import json
import glob

class CPTVUploader:
    def __init__(self):
        self.url = None        
        self.source_dir = None
        self.device_name = None
        self.device_password = None

    def process(self):
        print('Uploading to  ', self.url)
        api = DeviceAPI(self.url, self.device_name, self.device_password).login()

        files = self._find_files_to_upload()
        for file in files:
            self._uploadfile(api, file)

    def _uploadfile(self, api, filename):
        props = self._readPropertiesFromFile(filename)

        api.upload_recording(filename, props)


    def _uploader(self, queue, api):
        while True:
            
            filename = queue.get()

            if filename is None:
                break

            try:
                _uploadfile(api, filename)

            finally:
                queue.task_done()

    def _find_files_to_upload(self):
        cptvfiles = glob.glob(os.path.join(self.source_dir, '**', '*.cptv'), recursive=True)
        
        return cptvfiles

    def _readPropertiesFromFile(self, filename): 
        basefile = os.path.splitext(filename)[0]
        jsonfilename = basefile + '.txt'

        if (os.path.isfile(jsonfilename)):
            with open(jsonfilename, 'r') as propsfile: 

                oldprops = json.load(propsfile)

                # List of properties to transfer.   Many such as Id, we don't want to transfer. 
                propTypesToTransfer = ("batteryCharging", "additionalMetadata", "comment", "location", 
                            "fileSize", "batteryLevel", "duration", "rawFileSize", "airplaneModeOn", 
                            "version", "recordingDateTime", "fileMimeType", "type")

                newProps = dict()

                for key in propTypesToTransfer: 
                    if oldprops.get(key) is not None:
                        newProps[key] = oldprops[key]

                newProps["comment"] = 'uploaded from "' + filename + '"'
                
                # Tags can't be imported at the moment - maybe because there is no tagger Id. 

                # if ('Tags' in oldprops and oldprops['Tags'] is not None):
                #   tags = oldprops['Tags']
                #     tagPropTypesToTransfer = ("confidence", "number", "sex", "updatedAt", "startTime", 
                #         "age","automatic", "createdAt", "trapType", "event", "animal", "duration")
                #     newTags = list()

                #     for tag in tags:
                #         newTagProps = dict()
                #         for key in tagPropTypesToTransfer: 
                #             if (key in tag and tag[key] is not None):
                #                 newTagProps[key] = tag[key]
                #         newTags += newTagProps                    
                #     newProps['Tags'] = newTagProps

                return json.dumps(newProps)
        
        return None


def main(): 
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--password',
        dest='device_password',
        default='password',
        help='Password for the device')

    parser.add_argument('server_url',  help='Server (base) url to send the CPTV files to')
    
    parser.add_argument('source_dir',  help='Root folder where files for upload are stored')
    
    parser.add_argument('device_name',  help='Device identifier to upload recordings under')

    uploader = CPTVUploader()

    args = parser.parse_args()

    uploader.url = args.server_url
    uploader.source_dir = args.source_dir
    uploader.device_name = args.device_name
    uploader.device_password = args.device_password

    uploader.process()



if __name__ == '__main__':
    main()