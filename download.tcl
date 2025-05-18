proc downloadFile {url} {
  set destination "C:/windows/temp/putty.exe"
  set command "curl --output $destination $url"
  set result [catch {exec {*}$command} output]

  if {$result != 0} {
    puts "Error: $output"
  } else {
    puts "File downloaded successfully to $destination."
  }
}

set url "https://the.earth.li/~sgtatham/putty/0.78/w64/putty.exe"
downloadFile $url
exit
