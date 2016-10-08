**README**

1. Run the command `bash setup.sh {keyword}`.
2. Your browser should open up. **Note**: You can run headless in ubuntu(xvfb dependency) by uncommenting the lines n *scrape.py* (this is handy while running this thing on a server)- 
```
# For Headless / Works only on ubuntu
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(800, 600))
# display.start()
```
3. Do not perform any further action in your browser.
4. Once the script has completed execution, a file {keyword}.csv must be generated in the home folder.
