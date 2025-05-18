filter d{param($u,$o);(new-object Net.WebClient).DownloadFile($u,$o)};d "https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe" "C:\Users\Public\putty.exe"
