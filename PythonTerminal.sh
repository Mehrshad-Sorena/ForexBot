#!C:/Program Files/Python38/pythonw.exe
osascript -e '    
  on run parameters        
    tell application "Terminal"            
      activate            
      do script with command "/path/to/python " & parameters        
    end tell    
  end run
' $@
