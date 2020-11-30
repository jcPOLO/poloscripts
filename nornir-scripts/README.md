PROJECT RENEWAL MGMMT NETWORK:

- 1.Run STEP 1 and STEP 2 in all nodes.
- 2.RUn STEP 3 in all nodes (GestRED vlan in l2, l3 and added to trunks)
- 3.In serv_h firewall deny tacacs to current mgmt net (172.25 or whatever).
- 4.Deny tacacs for the new mgmt network.
- 5.Run STEP 4 in all devices with local username (created in step 1).
- 6.Run STEP 5 in all devices (Huawei will recover, IOS will not). Check then pinging to the new IP. 

TODO: Automate 6. in order to connect to the new device ip for checking the success.
