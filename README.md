
1. BSP S3.pdf - LateX document of the Bachelor semester project entitled _Encryption algorithms for secure communication over the Internet_

2. PLSUM.pdf - Summary of the report in English

3. SLSUM.pdf - summary of report in French

4. PL-VIDEO - 15 min video in English

5. SL-VIDEO - 5 min video in French

Open a terminal or command prompt, navigate to the directory that contains your scripts, and run the server: python3 server.py 

6. server.py - this file should be run first; the server is listening for incoming connections and waiting for client to send messages; the server receives the ciphertext. Once, on server terminal window, choose from menu the same algorithm used during encryption in order to recover the plaintext that shall be automatically sent over to the client.

After you have run the server, open a terminal or command prompt, navigate to the directory that contains your scripts, and run the client: python3 client.py 

7. client.py - follow the menu options (1) choose encryption algorithm from 1,2,3,4 or type 5 to exit. Type in your message to be encrypted and then sent over to the server by clicking _Enter_.
