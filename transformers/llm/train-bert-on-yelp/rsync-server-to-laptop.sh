 
# rsync the "ai" directory from server to laptop
# remove the --dry-run

rsync --dry-run --verbose --mkpath --archive /home/mzimmermann/dev/my-projects-source/public-on-github/ai mzimmermann@acer-ryzen-laptop-wifi:~/dev/my-projects-source/public-on-github
