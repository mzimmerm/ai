# From https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533
import torch, grp, pwd, os, subprocess
import numpy as np
import getpass
devices = []
try:
	print("\n\nChecking ROCM support...")
	result = subprocess.run(['rocminfo'], stdout=subprocess.PIPE)
	cmd_str = result.stdout.decode('utf-8')
	cmd_split = cmd_str.split('Agent ')
	for part in cmd_split:
		item_single = part[0:1]
		item_double = part[0:2]
		if item_single.isnumeric() or item_double.isnumeric():
			new_split = cmd_str.split('Agent '+item_double)
			device = new_split[1].split('Marketing Name:')[0].replace('  Name:                    ', '').replace('\n','').replace('                  ','').split('Uuid:')[0].split('*******')[1]
			devices.append(device)
	if len(devices) > 0:
		print('GOOD: ROCM devices found: ', len(devices))
	else:
		print('BAD: No ROCM devices found.')

	print("Checking PyTorch...")
	x = torch.rand(5, 3)
	has_torch = False
	len_x = len(x)
	if len_x == 5:
		has_torch = True
		for i in x:
			if len(i) == 3:
				has_torch = True
			else:
				has_torch = False
	if has_torch:
		print('GOOD: PyTorch is working fine.')
	else:
		print('BAD: PyTorch is NOT working.')


	print("Checking user groups...")
	user = getpass.getuser()
	groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
	gid = pwd.getpwnam(user).pw_gid
	groups.append(grp.getgrgid(gid).gr_name)
	if 'render' in groups and 'video' in groups:
		print('GOOD: The user', user, 'is in RENDER and VIDEO groups.')
	else:
		print('BAD: The user', user, 'is NOT in RENDER and VIDEO groups. This is necessary in order to PyTorch use HIP resources')

	if torch.cuda.is_available():
		print("GOOD: PyTorch ROCM support found.")

                torch.zeros([2, 4], dtype=torch.int32)
                torch.tensor(np.array([[1, 2, 3], [4, 5, 6]]))
                x = torch.tensor([[1, 2, 3], [4, 5, 6]])
                print(x[1][2])
                x = torch.tensor([[1]])
                x
                cuda0 = torch.device('cuda:0')
                torch.ones([2, 4], dtype=torch.float64, device=cuda0)
                
                t = torch.tensor([5, 5, 5], dtype=torch.int64, device=cuda0)
		print('Testing PyTorch ROCM support...')
		if str(t) == "tensor([5, 5, 5], device='cuda:0')":
			print('Everything fine! You can run PyTorch code inside of: ')
			for device in devices:
				print('---> ', device)
	else:
		print("BAD: PyTorch ROCM support NOT found.")
except:
	print('Cannot find rocminfo command information. Unable to determine if AMDGPU drivers with ROCM support were installed.')
