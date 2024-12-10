#!/bin/bash

VenvDir=$1
ServiceName="marvin"
ServicePath="tbot_${ServiceName}.service"
MarvinMain="main.py"
WorkingDir=`pwd`
User=`whoami`

TokensPath=$(realpath $WorkingDir/tokens.json)

rm -rf $ServicePath

echo "[Unit]" >> $ServicePath
echo "Description=Telegram Bot ${ServiceName} Service" >> $ServicePath
echo "After=network.target" >> $ServicePath
echo "" >> $ServicePath
echo "[Service]" >> $ServicePath
echo "Type=simple" >> $ServicePath
echo "User=${User}" >> $ServicePath
echo "Group=${User}" >> $ServicePath
echo "Environment=\"TOKENS=${TokensPath}\"" >> $ServicePath
echo "WorkingDirectory=${WorkingDir}" >> $ServicePath
echo "ExecStart=${VenvDir}/bin/python ${WorkingDir}/${MarvinMain}" >> $ServicePath
#StandardOutput=append:/path/to/output.log
#StandardError=append:/path/to/error.log
echo "Restart=always" >> $ServicePath
echo "Environment=PYTHONUNBUFFERED=1" >> $ServicePath
echo "" >> $ServicePath

echo "[Install]" >> $ServicePath
echo "WantedBy=multi-user.target" >> $ServicePath

cp $ServicePath /etc/systemd/system/
systemctl daemon-reload

echo "To start service : sudo systemctl start ${ServicePath}"
echo "To stop service : sudo systemctl stop ${ServicePath}"
echo "To restart service : sudo systemctl restart ${ServicePath}"
echo "Logs : journalctl -u ${ServicePath} -f"

#rm -rf $ServicePath