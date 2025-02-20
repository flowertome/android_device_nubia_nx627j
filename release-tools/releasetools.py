# Copyright (C) 2015 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Emit commands needed for nubia Z20 during OTA installation
(installing the tz/xbl_config/xbl/hyp/modem/cmnlib/cmnlib64/dsp/qupfw/keymaster/bluetooth/aop/abl/devcfg/splash/uefisecapp/parameter/storsec/ImageFv/dtbo images)."""

import common
import re
import sha

def FullOTA_Assertions(info):
  print "FullOTA_Assertions not implemented"

def IncrementalOTA_Assertions(info):
  print "IncrementalOTA_Assertions not implemented"

def InstallImage(img_name, img_file, partition, info):
  common.ZipWriteStr(info.output_zip, img_name, img_file)
  info.script.AppendExtra(('package_extract_file("' + img_name + '", "/dev/block/bootdevice/by-name/' + partition + '");'))

image_partitions = {
   'tz.mbn'                   : 'tz',
   'xbl_config.elf'           : 'xbl_config',
   'xbl.elf'                  : 'xbl',
   'hyp.mbn'                  : 'hyp',
   'NON-HLOS.bin'             : 'modem',
   'cmnlib.mbn'               : 'cmnlib',
   'cmnlib64.mbn'             : 'cmnlib64',
   'dspso.bin'                : 'dsp',
   'qupv3fw.elf'              : 'qupfw',
   'km4.mbn'                  : 'keymaster',
   'BTFM.bin'                 : 'bluetooth',
   'aop.mbn'                  : 'aop',
   'abl.elf'                  : 'abl',
   'devcfg.mbn'               : 'devcfg',
   'splash.img'               : 'splash',
   'uefi_sec.mbn'             : 'uefisecapp',
   'parameter.img'            : 'parameter',
   'storsec.mbn'              : 'storsec',
   'imagefv.elf'              : 'ImageFv',
   'dtbo.img'                 : 'dtbo'
}

def FullOTA_InstallEnd(info):
  info.script.Print("Writing radio image...")
  for k, v in image_partitions.iteritems():
    try:
      img_file = info.input_zip.read("RADIO/" + k)
      info.script.Print("update image " + k + "...")
      InstallImage(k, img_file, v, info)
    except KeyError:
      print "warning: no " + k + " image in input target_files; not flashing " + k


def IncrementalOTA_InstallEnd(info):
  for k, v in image_partitions.iteritems():
    try:
      source_file = info.source_zip.read("RADIO/" + k)
      target_file = info.target_zip.read("RADIO/" + k)
      if source_file != target_file:
        InstallImage(k, target_file, v, info)
      else:
        print k + " image unchanged; skipping"
    except KeyError:
      print "warning: " + k + " image missing from target; not flashing " + k
