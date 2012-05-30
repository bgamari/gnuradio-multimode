import math
scan_low=0.0
scan_high=0.0
current_freq=0.0
last_ifreq=0.0
last_ena=False
triggered=0
last_returned=0.0
last_freq1=0.0
last_freq2=0.0
current_index=0
def scan_freq_out(ena,low,high,freq1,freq2,pwr,scan_thresh,incr,scan_rate,lst_mode,sclist):
	global scan_low
	global scan_high
	global current_freq
	global last_ifreq
	global last_clicked
	global last_ena
	global triggered
	global last_returned
	global last_freq1
	global last_freq2
	global current_index
	
	x = math.log(pwr)/math.log(10.0)
	x = x * 10.0
	
	if ena == True and lst_mode == True and len(sclist) > 0:
		if last_ena == False:
			current_index = 0
			triggered = 0
		last_ena = ena
		last_returned = sclist[current_index]

		if triggered > 0:
			triggered = triggered -1
			return last_returned
			
		elif x >= scan_thresh:
			triggered=(scan_rate*2)+1
			return last_returned
			
		current_index = current_index + 1
		if current_index > len(sclist)-1:
			current_index = 0
			
		return last_returned
	
	if ena == True and lst_mode == False:
		if last_ena == False:
			current_freq = low - incr
			triggered = 0
		last_ena = ena
		
		if scan_low != low or scan_high != high:
			current_freq = low - incr
			scan_low = low
			scan_high = high
			triggered = 0
			
		if triggered > 0:
			triggered = triggered - 1
			last_returned = current_freq
			return current_freq
			
		elif x >= scan_thresh:
			triggered=(scan_rate*2)+1
			last_returned = current_freq
			return current_freq
			
		current_freq = current_freq + incr
		if current_freq > high:
			current_freq = low - incr
		last_returned = current_freq
		return current_freq
	else:
		last_ena = ena
		if last_freq1 != freq1:
			last_freq1 = freq1
			last_returned = last_freq1
		elif last_freq2 != freq2:
			last_freq2 = freq2
			last_returned = last_freq2
		return last_returned

def get_last_returned(poll):
	global last_returned
	return last_returned
	
