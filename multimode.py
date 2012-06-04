#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Multimode Radio Receiver
# Author: Marcus D. Leech (patchvonbraun), Science Radio Laboratories, Inc.
# Generated: Mon Jun  4 18:11:15 2012
##################################################

from gnuradio import audio
from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import multimode_helper as mh
import osmosdr
import threading
import time
import wx

class multimode(grc_wxgui.top_block_gui):

	def __init__(self, ahw="default", freq=150.0e6, ppm=0.0, vol=1.0, ftune=0.0, xftune=0.0, srate=1.0e6, upclo=0.0, devinfo="rtl=0", agc=0, arate=48.0e3, upce=0, mbw=2.0e3, mthresh=-10.0, flist="", dmode="NFM1", offs=50.e3):
		grc_wxgui.top_block_gui.__init__(self, title="Multimode Radio Receiver")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.ahw = ahw
		self.freq = freq
		self.ppm = ppm
		self.vol = vol
		self.ftune = ftune
		self.xftune = xftune
		self.srate = srate
		self.upclo = upclo
		self.devinfo = devinfo
		self.agc = agc
		self.arate = arate
		self.upce = upce
		self.mbw = mbw
		self.mthresh = mthresh
		self.flist = flist
		self.dmode = dmode
		self.offs = offs

		##################################################
		# Variables
		##################################################
		self.sc_list_str = sc_list_str = flist
		self.thresh = thresh = mthresh
		self.scan_rate = scan_rate = 15
		self.scan_power = scan_power = 0
		self.sc_low = sc_low = 150e6
		self.sc_listm = sc_listm = False
		self.sc_list = sc_list = eval("["+sc_list_str+"]")
		self.sc_incr = sc_incr = 12.5e3
		self.sc_high = sc_high = 300e6
		self.sc_ena = sc_ena = False
		self.rf_power = rf_power = 0
		self.ifreq = ifreq = freq
		self.wbfm = wbfm = 200e3
		self.rf_d_power = rf_d_power = 0
		self.mode = mode = dmode
		self.logpower = logpower = math.log10(rf_power+1.0e-12)*10.0
		self.israte = israte = srate
		self.deviation_dict = deviation_dict = {'NFM1' : 5.0e3, 'NFM2' : 2.0e3, 'WFM' : 80e3, 'TV-FM' : 25e3, 'AM' : 9e3, 'USB' : 9e3, 'LSB' : 9e3}
		self.cur_freq = cur_freq = mh.scan_freq_out(sc_ena,sc_low,sc_high,freq,ifreq,scan_power+1.0e-14,thresh,sc_incr,scan_rate,sc_listm,sc_list)
		self.bw = bw = mbw
		self.xfine = xfine = xftune
		self.volume = volume = vol
		self.variable_static_text_1 = variable_static_text_1 = cur_freq
		self.variable_static_text_0 = variable_static_text_0 = float(int(math.log10(rf_d_power+1.0e-14)*100.0)/10.0)
		self.upc_offset = upc_offset = upclo
		self.upc = upc = upce
		self.ssb_modes = ssb_modes = ["USB", "LSB"]
		self.sc_list_len = sc_list_len = len(sc_list)
		self.samp_rate = samp_rate = int(int(israte/wbfm)*wbfm)
		self.rfgain = rfgain = 25
		self.record_file = record_file = "recording.wav"
		self.record = record = False
		self.offset = offset = offs
		self.muted = muted = 0.0 if logpower >= thresh else 1
		self.k = k = wbfm/(2*math.pi*deviation_dict[mode])
		self.iagc = iagc = agc
		self.freq_update = freq_update = 0
		self.fm_modes = fm_modes = ["NFM1", "NFM2", "WFM", "TV-FM"]
		self.fm_mode_labels = fm_mode_labels = ["NFM1(5kHz)", "NFM2(2.5Khz)", "WFM(80Khz)", "TV-FM(25Khz)"]
		self.fine = fine = ftune
		self.audio_int_rate = audio_int_rate = 25e3
		self.am_modes = am_modes = ["AM"]
		self.am_filt_dict_low = am_filt_dict_low = {'AM' : -bw/2, 'USB' : bw/12, 'LSB': -bw/2, 'NFM1' : -bw/2, 'NFM2' : -bw/2, 'WFM' : -bw/2, 'TV-FM' : -bw/2}
		self.am_filt_dict_high = am_filt_dict_high = {'AM' : bw/2, 'USB' : bw/2, 'LSB': -bw/12, 'NFM1' : bw/2, 'NFM2' : bw/2, 'WFM' : bw/2, 'TV-FM' : bw/2}
		self.adjusted = adjusted = "" if int(srate) % int(wbfm) == 0 else " (adjusted)"

		##################################################
		# Blocks
		##################################################
		self.rf_probe = gr.probe_avg_mag_sqrd_c(0, 0.05)
		self.Main = self.Main = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.Main.AddPage(grc_wxgui.Panel(self.Main), "Main Controls")
		self.Main.AddPage(grc_wxgui.Panel(self.Main), "Scan/Upconv Controls/Detail")
		self.Add(self.Main)
		_xfine_sizer = wx.BoxSizer(wx.VERTICAL)
		self._xfine_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_xfine_sizer,
			value=self.xfine,
			callback=self.set_xfine,
			label="Extra Fine Tuning",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._xfine_slider = forms.slider(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_xfine_sizer,
			value=self.xfine,
			callback=self.set_xfine,
			minimum=-1.0e3,
			maximum=1.0e3,
			num_steps=200,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Main.GetPage(0).GridAdd(_xfine_sizer, 0, 3, 1, 1)
		_volume_sizer = wx.BoxSizer(wx.VERTICAL)
		self._volume_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_volume_sizer,
			value=self.volume,
			callback=self.set_volume,
			label="Volume",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._volume_slider = forms.slider(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_volume_sizer,
			value=self.volume,
			callback=self.set_volume,
			minimum=1.0,
			maximum=10.0,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Main.GetPage(0).GridAdd(_volume_sizer, 0, 0, 1, 1)
		self._upc_offset_text_box = forms.text_box(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.upc_offset,
			callback=self.set_upc_offset,
			label="Upconv. LO Freq",
			converter=forms.float_converter(),
		)
		self.Main.GetPage(1).GridAdd(self._upc_offset_text_box, 3, 2, 1, 2)
		self._upc_check_box = forms.check_box(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.upc,
			callback=self.set_upc,
			label="Ext. Upconv.",
			true=1,
			false=0,
		)
		self.Main.GetPage(1).GridAdd(self._upc_check_box, 3, 0, 1, 1)
		_rfgain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._rfgain_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_rfgain_sizer,
			value=self.rfgain,
			callback=self.set_rfgain,
			label="RF Gain",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._rfgain_slider = forms.slider(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_rfgain_sizer,
			value=self.rfgain,
			callback=self.set_rfgain,
			minimum=0,
			maximum=50,
			num_steps=200,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Main.GetPage(0).GridAdd(_rfgain_sizer, 2, 1, 1, 1)
		self._record_file_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			value=self.record_file,
			callback=self.set_record_file,
			label="Recording Filename",
			converter=forms.str_converter(),
		)
		self.Main.GetPage(0).GridAdd(self._record_file_text_box, 2, 3, 1, 3)
		self._record_check_box = forms.check_box(
			parent=self.Main.GetPage(0).GetWin(),
			value=self.record,
			callback=self.set_record,
			label="Record",
			true=True,
			false=False,
		)
		self.Main.GetPage(0).GridAdd(self._record_check_box, 2, 2, 1, 1)
		_offset_sizer = wx.BoxSizer(wx.VERTICAL)
		self._offset_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_offset_sizer,
			value=self.offset,
			callback=self.set_offset,
			label="LO Offset",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._offset_slider = forms.slider(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_offset_sizer,
			value=self.offset,
			callback=self.set_offset,
			minimum=25e3,
			maximum=500e3,
			num_steps=200,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Main.GetPage(0).GridAdd(_offset_sizer, 1, 3, 1, 1)
		self._mode_chooser = forms.drop_down(
			parent=self.Main.GetPage(0).GetWin(),
			value=self.mode,
			callback=self.set_mode,
			label="Mode",
			choices=fm_modes+am_modes+ssb_modes,
			labels=fm_mode_labels+am_modes+ssb_modes,
		)
		self.Main.GetPage(0).GridAdd(self._mode_chooser, 0, 4, 1, 1)
		self._iagc_check_box = forms.check_box(
			parent=self.Main.GetPage(0).GetWin(),
			value=self.iagc,
			callback=self.set_iagc,
			label="AGC",
			true=1,
			false=0,
		)
		self.Main.GetPage(0).GridAdd(self._iagc_check_box, 2, 0, 1, 1)
		def _freq_update_probe():
			while True:
				val = self.rf_probe.level()
				try: self.set_freq_update(val)
				except AttributeError, e: pass
				time.sleep(1.0/(1.0/(2.5)))
		_freq_update_thread = threading.Thread(target=_freq_update_probe)
		_freq_update_thread.daemon = True
		_freq_update_thread.start()
		_fine_sizer = wx.BoxSizer(wx.VERTICAL)
		self._fine_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_fine_sizer,
			value=self.fine,
			callback=self.set_fine,
			label="Fine Tuning",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._fine_slider = forms.slider(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_fine_sizer,
			value=self.fine,
			callback=self.set_fine,
			minimum=-35e3,
			maximum=35e3,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Main.GetPage(0).GridAdd(_fine_sizer, 0, 2, 1, 1)
		self.display_probe = gr.probe_avg_mag_sqrd_c(0, 0.005)
		_bw_sizer = wx.BoxSizer(wx.VERTICAL)
		self._bw_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_bw_sizer,
			value=self.bw,
			callback=self.set_bw,
			label="AM/SSB Bandwidth",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._bw_slider = forms.slider(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_bw_sizer,
			value=self.bw,
			callback=self.set_bw,
			minimum=1.0e3,
			maximum=audio_int_rate/2,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Main.GetPage(0).GridAdd(_bw_sizer, 1, 2, 1, 1)
		self.wxgui_waterfallsink2_0_0 = waterfallsink2.waterfall_sink_c(
			self.Main.GetPage(1).GetWin(),
			baseband_freq=0,
			dynamic_range=40,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=audio_int_rate,
			fft_size=2048,
			fft_rate=4,
			average=True,
			avg_alpha=None,
			title="Detailed Spectrogram",
			win=window.hamming,
		)
		self.Main.GetPage(1).Add(self.wxgui_waterfallsink2_0_0.win)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.Main.GetPage(0).GetWin(),
			baseband_freq=mh.get_last_returned(freq_update),
			dynamic_range=40,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=6,
			average=True,
			avg_alpha=None,
			title="Spectrogram",
			win=window.hamming,
		)
		self.Main.GetPage(0).Add(self.wxgui_waterfallsink2_0.win)
		def wxgui_waterfallsink2_0_callback(x, y):
			self.set_freq(x)
		
		self.wxgui_waterfallsink2_0.set_callback(wxgui_waterfallsink2_0_callback)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.Main.GetPage(0).GetWin(),
			baseband_freq=mh.get_last_returned(freq_update),
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=6,
			average=True,
			avg_alpha=0.1,
			title="Panorama",
			peak_hold=False,
			win=window.hamming,
		)
		self.Main.GetPage(0).Add(self.wxgui_fftsink2_0.win)
		def wxgui_fftsink2_0_callback(x, y):
			self.set_freq(x)
		
		self.wxgui_fftsink2_0.set_callback(wxgui_fftsink2_0_callback)
		self._variable_static_text_1_static_text = forms.static_text(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.variable_static_text_1,
			callback=self.set_variable_static_text_1,
			label="Current Scan Freq",
			converter=forms.float_converter(),
		)
		self.Main.GetPage(1).GridAdd(self._variable_static_text_1_static_text, 0, 5, 1, 2)
		self._variable_static_text_0_static_text = forms.static_text(
			parent=self.Main.GetPage(0).GetWin(),
			value=self.variable_static_text_0,
			callback=self.set_variable_static_text_0,
			label="RF Level",
			converter=forms.float_converter(),
		)
		self.Main.GetPage(0).GridAdd(self._variable_static_text_0_static_text, 1, 0, 1, 1)
		_thresh_sizer = wx.BoxSizer(wx.VERTICAL)
		self._thresh_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_thresh_sizer,
			value=self.thresh,
			callback=self.set_thresh,
			label="Mute Threshold",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._thresh_slider = forms.slider(
			parent=self.Main.GetPage(0).GetWin(),
			sizer=_thresh_sizer,
			value=self.thresh,
			callback=self.set_thresh,
			minimum=-50,
			maximum=10,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Main.GetPage(0).GridAdd(_thresh_sizer, 1, 1, 1, 1)
		def _scan_power_probe():
			while True:
				val = self.rf_probe.level()
				try: self.set_scan_power(val)
				except AttributeError, e: pass
				time.sleep(1.0/(scan_rate))
		_scan_power_thread = threading.Thread(target=_scan_power_probe)
		_scan_power_thread.daemon = True
		_scan_power_thread.start()
		self._sc_low_text_box = forms.text_box(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.sc_low,
			callback=self.set_sc_low,
			label="Scan Low",
			converter=forms.float_converter(),
		)
		self.Main.GetPage(1).GridAdd(self._sc_low_text_box, 0, 1, 1, 1)
		self._sc_listm_check_box = forms.check_box(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.sc_listm,
			callback=self.set_sc_listm,
			label="Scan List Mode",
			true=True,
			false=False,
		)
		self.Main.GetPage(1).GridAdd(self._sc_listm_check_box, 2, 0, 1, 1)
		self._sc_list_str_text_box = forms.text_box(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.sc_list_str,
			callback=self.set_sc_list_str,
			label="Scan List",
			converter=forms.str_converter(),
		)
		self.Main.GetPage(1).GridAdd(self._sc_list_str_text_box, 2, 1, 1, 5)
		self._sc_incr_chooser = forms.drop_down(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.sc_incr,
			callback=self.set_sc_incr,
			label="Scan Increment (Hz)",
			choices=[5.0e3,6.25e3,10.0e3,12.5e3,15e3,25e3],
			labels=[],
		)
		self.Main.GetPage(1).GridAdd(self._sc_incr_chooser, 0, 0, 1, 1)
		self._sc_high_text_box = forms.text_box(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.sc_high,
			callback=self.set_sc_high,
			label="Scan High",
			converter=forms.float_converter(),
		)
		self.Main.GetPage(1).GridAdd(self._sc_high_text_box, 0, 2, 1, 1)
		self._sc_ena_check_box = forms.check_box(
			parent=self.Main.GetPage(1).GetWin(),
			value=self.sc_ena,
			callback=self.set_sc_ena,
			label="Scan Enable",
			true=True,
			false=False,
		)
		self.Main.GetPage(1).GridAdd(self._sc_ena_check_box, 0, 3, 1, 1)
		def _rf_power_probe():
			while True:
				val = self.rf_probe.level()
				try: self.set_rf_power(val)
				except AttributeError, e: pass
				time.sleep(1.0/(10))
		_rf_power_thread = threading.Thread(target=_rf_power_probe)
		_rf_power_thread.daemon = True
		_rf_power_thread.start()
		def _rf_d_power_probe():
			while True:
				val = self.display_probe.level()
				try: self.set_rf_d_power(val)
				except AttributeError, e: pass
				time.sleep(1.0/(5))
		_rf_d_power_thread = threading.Thread(target=_rf_d_power_probe)
		_rf_d_power_thread.daemon = True
		_rf_d_power_thread.start()
		self.osmosdr_source_c_0 = osmosdr.source_c( args="nchan=" + str(1) + " " + devinfo  )
		self.osmosdr_source_c_0.set_sample_rate(samp_rate)
		self.osmosdr_source_c_0.set_center_freq(cur_freq+offset+(upc_offset*float(upc)), 0)
		self.osmosdr_source_c_0.set_freq_corr(ppm, 0)
		self.osmosdr_source_c_0.set_gain_mode(iagc, 0)
		self.osmosdr_source_c_0.set_gain(25 if iagc == 1 else rfgain, 0)
		self.low_pass_filter_3 = gr.fir_filter_ccf(int(wbfm/audio_int_rate), firdes.low_pass(
			1, wbfm, 11.5e3, 7.5e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_2 = gr.fir_filter_fff(int(wbfm/audio_int_rate), firdes.low_pass(
			1, wbfm, 11.5e3, 4.5e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_1 = gr.fir_filter_ccf(4, firdes.low_pass(
			1, samp_rate, 98e3, 55e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0 = gr.fir_filter_ccf(1, firdes.low_pass(
			1, wbfm, deviation_dict[mode]*1.15, deviation_dict[mode]/1.85, firdes.WIN_HAMMING, 6.76))
		self._israte_chooser = forms.drop_down(
			parent=self.Main.GetPage(0).GetWin(),
			value=self.israte,
			callback=self.set_israte,
			label="Samp Rate",
			choices=[1.0e6,1.4e6,1.8e6,2.0e6,2.4e6,2.8e6],
			labels=["1M", "1.4M", "1.8M", "2.0M", "2.4M", "2.8M"],
		)
		self.Main.GetPage(0).GridAdd(self._israte_chooser, 1, 4, 1, 1)
		self._ifreq_text_box = forms.text_box(
			parent=self.Main.GetPage(0).GetWin(),
			value=self.ifreq,
			callback=self.set_ifreq,
			label="Frequency",
			converter=forms.float_converter(),
		)
		self.Main.GetPage(0).GridAdd(self._ifreq_text_box, 0, 1, 1, 1)
		self.gr_wavfile_sink_0 = gr.wavfile_sink("/dev/null" if record == False else record_file, 1, int(audio_int_rate), 8)
		self.gr_quadrature_demod_cf_0 = gr.quadrature_demod_cf(k)
		self.gr_multiply_const_vxx_2 = gr.multiply_const_vff((1.0 if mode in fm_modes else 0.0, ))
		self.gr_multiply_const_vxx_1 = gr.multiply_const_vff((0.0 if muted else volume/4.5, ))
		self.gr_multiply_const_vxx_0_0_0 = gr.multiply_const_vff((1.0 if mode in am_modes else 0.0, ))
		self.gr_multiply_const_vxx_0_0 = gr.multiply_const_vff((1.25 if mode in ssb_modes else 0.0, ))
		self.gr_keep_one_in_n_0 = gr.keep_one_in_n(gr.sizeof_gr_complex*1, int(wbfm/audio_int_rate))
		self.gr_freq_xlating_fir_filter_xxx_0_1 = gr.freq_xlating_fir_filter_ccc(1, (1.0, ), offset+fine+xfine, samp_rate)
		self.gr_fractional_interpolator_xx_1 = gr.fractional_interpolator_cc(0, (samp_rate/4)/wbfm)
		self.gr_fractional_interpolator_xx_0 = gr.fractional_interpolator_ff(0, audio_int_rate/arate)
		self.gr_feedforward_agc_cc_0 = gr.feedforward_agc_cc(512, 0.75)
		self.gr_complex_to_real_0 = gr.complex_to_real(1)
		self.gr_complex_to_mag_squared_0 = gr.complex_to_mag_squared(1)
		self.gr_agc2_xx_0 = gr.agc2_cc(1e-2, 1e-3, 0.75, 1.0, 0.0)
		self.gr_add_xx_0 = gr.add_vff(1)
		self.blks2_fm_deemph_0 = blks2.fm_deemph(fs=audio_int_rate, tau=75e-6)
		self.band_pass_filter_1 = gr.fir_filter_fff(1, firdes.band_pass(
			1.25, audio_int_rate, 100, 6.0e3, 2.5e3, firdes.WIN_HAMMING, 6.76))
		self.band_pass_filter_0 = gr.fir_filter_ccc(1, firdes.complex_band_pass(
			1.0, audio_int_rate, am_filt_dict_low[mode], am_filt_dict_high[mode], bw/2.5, firdes.WIN_HAMMING, 6.76))
		self.audio_sink_0 = audio.sink(int(arate), ahw, True)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_multiply_const_vxx_0_0, 0), (self.gr_add_xx_0, 1))
		self.connect((self.gr_fractional_interpolator_xx_0, 0), (self.gr_multiply_const_vxx_1, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0_1, 0), (self.wxgui_waterfallsink2_0, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.audio_sink_0, 1))
		self.connect((self.gr_add_xx_0, 0), (self.gr_fractional_interpolator_xx_0, 0))
		self.connect((self.gr_add_xx_0, 0), (self.gr_wavfile_sink_0, 0))
		self.connect((self.gr_feedforward_agc_cc_0, 0), (self.gr_complex_to_mag_squared_0, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0_1, 0))
		self.connect((self.low_pass_filter_0, 0), (self.gr_quadrature_demod_cf_0, 0))
		self.connect((self.gr_quadrature_demod_cf_0, 0), (self.low_pass_filter_2, 0))
		self.connect((self.low_pass_filter_2, 0), (self.blks2_fm_deemph_0, 0))
		self.connect((self.blks2_fm_deemph_0, 0), (self.gr_multiply_const_vxx_2, 0))
		self.connect((self.gr_multiply_const_vxx_0_0_0, 0), (self.gr_add_xx_0, 2))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0_1, 0), (self.low_pass_filter_1, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0_1, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.gr_complex_to_mag_squared_0, 0), (self.band_pass_filter_1, 0))
		self.connect((self.band_pass_filter_1, 0), (self.gr_multiply_const_vxx_0_0_0, 0))
		self.connect((self.gr_agc2_xx_0, 0), (self.low_pass_filter_0, 0))
		self.connect((self.gr_keep_one_in_n_0, 0), (self.display_probe, 0))
		self.connect((self.gr_keep_one_in_n_0, 0), (self.rf_probe, 0))
		self.connect((self.gr_keep_one_in_n_0, 0), (self.band_pass_filter_0, 0))
		self.connect((self.gr_feedforward_agc_cc_0, 0), (self.gr_complex_to_real_0, 0))
		self.connect((self.band_pass_filter_0, 0), (self.gr_feedforward_agc_cc_0, 0))
		self.connect((self.gr_multiply_const_vxx_2, 0), (self.gr_add_xx_0, 0))
		self.connect((self.gr_complex_to_real_0, 0), (self.gr_multiply_const_vxx_0_0, 0))
		self.connect((self.low_pass_filter_3, 0), (self.wxgui_waterfallsink2_0_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.gr_keep_one_in_n_0, 0))
		self.connect((self.low_pass_filter_1, 0), (self.gr_fractional_interpolator_xx_1, 0))
		self.connect((self.gr_fractional_interpolator_xx_1, 0), (self.gr_agc2_xx_0, 0))
		self.connect((self.gr_fractional_interpolator_xx_1, 0), (self.low_pass_filter_3, 0))

	def get_ahw(self):
		return self.ahw

	def set_ahw(self, ahw):
		self.ahw = ahw

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self.set_ifreq(self.freq)

	def get_ppm(self):
		return self.ppm

	def set_ppm(self, ppm):
		self.ppm = ppm
		self.osmosdr_source_c_0.set_freq_corr(self.ppm, 0)

	def get_vol(self):
		return self.vol

	def set_vol(self, vol):
		self.vol = vol
		self.set_volume(self.vol)

	def get_ftune(self):
		return self.ftune

	def set_ftune(self, ftune):
		self.ftune = ftune
		self.set_fine(self.ftune)

	def get_xftune(self):
		return self.xftune

	def set_xftune(self, xftune):
		self.xftune = xftune
		self.set_xfine(self.xftune)

	def get_srate(self):
		return self.srate

	def set_srate(self, srate):
		self.srate = srate
		self.set_adjusted("" if int(self.srate) % int(self.wbfm) == 0 else " (adjusted)")
		self.set_israte(self.srate)

	def get_upclo(self):
		return self.upclo

	def set_upclo(self, upclo):
		self.upclo = upclo
		self.set_upc_offset(self.upclo)

	def get_devinfo(self):
		return self.devinfo

	def set_devinfo(self, devinfo):
		self.devinfo = devinfo

	def get_agc(self):
		return self.agc

	def set_agc(self, agc):
		self.agc = agc
		self.set_iagc(self.agc)

	def get_arate(self):
		return self.arate

	def set_arate(self, arate):
		self.arate = arate
		self.gr_fractional_interpolator_xx_0.set_interp_ratio(self.audio_int_rate/self.arate)

	def get_upce(self):
		return self.upce

	def set_upce(self, upce):
		self.upce = upce
		self.set_upc(self.upce)

	def get_mbw(self):
		return self.mbw

	def set_mbw(self, mbw):
		self.mbw = mbw
		self.set_bw(self.mbw)

	def get_mthresh(self):
		return self.mthresh

	def set_mthresh(self, mthresh):
		self.mthresh = mthresh
		self.set_thresh(self.mthresh)

	def get_flist(self):
		return self.flist

	def set_flist(self, flist):
		self.flist = flist
		self.set_sc_list_str(self.flist)

	def get_dmode(self):
		return self.dmode

	def set_dmode(self, dmode):
		self.dmode = dmode
		self.set_mode(self.dmode)

	def get_offs(self):
		return self.offs

	def set_offs(self, offs):
		self.offs = offs
		self.set_offset(self.offs)

	def get_sc_list_str(self):
		return self.sc_list_str

	def set_sc_list_str(self, sc_list_str):
		self.sc_list_str = sc_list_str
		self.set_sc_list(eval("["+self.sc_list_str+"]"))
		self._sc_list_str_text_box.set_value(self.sc_list_str)

	def get_thresh(self):
		return self.thresh

	def set_thresh(self, thresh):
		self.thresh = thresh
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self._thresh_slider.set_value(self.thresh)
		self._thresh_text_box.set_value(self.thresh)
		self.set_muted(0.0 if self.logpower >= self.thresh else 1)

	def get_scan_rate(self):
		return self.scan_rate

	def set_scan_rate(self, scan_rate):
		self.scan_rate = scan_rate
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))

	def get_scan_power(self):
		return self.scan_power

	def set_scan_power(self, scan_power):
		self.scan_power = scan_power
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))

	def get_sc_low(self):
		return self.sc_low

	def set_sc_low(self, sc_low):
		self.sc_low = sc_low
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self._sc_low_text_box.set_value(self.sc_low)

	def get_sc_listm(self):
		return self.sc_listm

	def set_sc_listm(self, sc_listm):
		self.sc_listm = sc_listm
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self._sc_listm_check_box.set_value(self.sc_listm)

	def get_sc_list(self):
		return self.sc_list

	def set_sc_list(self, sc_list):
		self.sc_list = sc_list
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self.set_sc_list_len(len(self.sc_list))

	def get_sc_incr(self):
		return self.sc_incr

	def set_sc_incr(self, sc_incr):
		self.sc_incr = sc_incr
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self._sc_incr_chooser.set_value(self.sc_incr)

	def get_sc_high(self):
		return self.sc_high

	def set_sc_high(self, sc_high):
		self.sc_high = sc_high
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self._sc_high_text_box.set_value(self.sc_high)

	def get_sc_ena(self):
		return self.sc_ena

	def set_sc_ena(self, sc_ena):
		self.sc_ena = sc_ena
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self._sc_ena_check_box.set_value(self.sc_ena)

	def get_rf_power(self):
		return self.rf_power

	def set_rf_power(self, rf_power):
		self.rf_power = rf_power
		self.set_logpower(math.log10(self.rf_power+1.0e-12)*10.0)

	def get_ifreq(self):
		return self.ifreq

	def set_ifreq(self, ifreq):
		self.ifreq = ifreq
		self.set_cur_freq(mh.scan_freq_out(self.sc_ena,self.sc_low,self.sc_high,self.freq,self.ifreq,self.scan_power+1.0e-14,self.thresh,self.sc_incr,self.scan_rate,self.sc_listm,self.sc_list))
		self._ifreq_text_box.set_value(self.ifreq)

	def get_wbfm(self):
		return self.wbfm

	def set_wbfm(self, wbfm):
		self.wbfm = wbfm
		self.set_adjusted("" if int(self.srate) % int(self.wbfm) == 0 else " (adjusted)")
		self.set_samp_rate(int(int(self.israte/self.wbfm)*self.wbfm))
		self.gr_keep_one_in_n_0.set_n(int(self.wbfm/self.audio_int_rate))
		self.gr_fractional_interpolator_xx_1.set_interp_ratio((self.samp_rate/4)/self.wbfm)
		self.set_k(self.wbfm/(2*math.pi*self.deviation_dict[self.mode]))
		self.low_pass_filter_3.set_taps(firdes.low_pass(1, self.wbfm, 11.5e3, 7.5e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_2.set_taps(firdes.low_pass(1, self.wbfm, 11.5e3, 4.5e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wbfm, self.deviation_dict[self.mode]*1.15, self.deviation_dict[self.mode]/1.85, firdes.WIN_HAMMING, 6.76))

	def get_rf_d_power(self):
		return self.rf_d_power

	def set_rf_d_power(self, rf_d_power):
		self.rf_d_power = rf_d_power
		self.set_variable_static_text_0(float(int(math.log10(self.rf_d_power+1.0e-14)*100.0)/10.0))

	def get_mode(self):
		return self.mode

	def set_mode(self, mode):
		self.mode = mode
		self.gr_multiply_const_vxx_0_0_0.set_k((1.0 if self.mode in self.am_modes else 0.0, ))
		self.gr_multiply_const_vxx_2.set_k((1.0 if self.mode in self.fm_modes else 0.0, ))
		self.gr_multiply_const_vxx_0_0.set_k((1.25 if self.mode in self.ssb_modes else 0.0, ))
		self._mode_chooser.set_value(self.mode)
		self.set_k(self.wbfm/(2*math.pi*self.deviation_dict[self.mode]))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wbfm, self.deviation_dict[self.mode]*1.15, self.deviation_dict[self.mode]/1.85, firdes.WIN_HAMMING, 6.76))
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1.0, self.audio_int_rate, self.am_filt_dict_low[self.mode], self.am_filt_dict_high[self.mode], self.bw/2.5, firdes.WIN_HAMMING, 6.76))

	def get_logpower(self):
		return self.logpower

	def set_logpower(self, logpower):
		self.logpower = logpower
		self.set_muted(0.0 if self.logpower >= self.thresh else 1)

	def get_israte(self):
		return self.israte

	def set_israte(self, israte):
		self.israte = israte
		self.set_samp_rate(int(int(self.israte/self.wbfm)*self.wbfm))
		self._israte_chooser.set_value(self.israte)

	def get_deviation_dict(self):
		return self.deviation_dict

	def set_deviation_dict(self, deviation_dict):
		self.deviation_dict = deviation_dict
		self.set_k(self.wbfm/(2*math.pi*self.deviation_dict[self.mode]))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wbfm, self.deviation_dict[self.mode]*1.15, self.deviation_dict[self.mode]/1.85, firdes.WIN_HAMMING, 6.76))

	def get_cur_freq(self):
		return self.cur_freq

	def set_cur_freq(self, cur_freq):
		self.cur_freq = cur_freq
		self.osmosdr_source_c_0.set_center_freq(self.cur_freq+self.offset+(self.upc_offset*float(self.upc)), 0)
		self.set_variable_static_text_1(self.cur_freq)

	def get_bw(self):
		return self.bw

	def set_bw(self, bw):
		self.bw = bw
		self._bw_slider.set_value(self.bw)
		self._bw_text_box.set_value(self.bw)
		self.set_am_filt_dict_high({'AM' : self.bw/2, 'USB' : self.bw/2, 'LSB': -self.bw/12, 'NFM1' : self.bw/2, 'NFM2' : self.bw/2, 'WFM' : self.bw/2, 'TV-FM' : self.bw/2})
		self.set_am_filt_dict_low({'AM' : -self.bw/2, 'USB' : self.bw/12, 'LSB': -self.bw/2, 'NFM1' : -self.bw/2, 'NFM2' : -self.bw/2, 'WFM' : -self.bw/2, 'TV-FM' : -self.bw/2})
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1.0, self.audio_int_rate, self.am_filt_dict_low[self.mode], self.am_filt_dict_high[self.mode], self.bw/2.5, firdes.WIN_HAMMING, 6.76))

	def get_xfine(self):
		return self.xfine

	def set_xfine(self, xfine):
		self.xfine = xfine
		self._xfine_slider.set_value(self.xfine)
		self._xfine_text_box.set_value(self.xfine)
		self.gr_freq_xlating_fir_filter_xxx_0_1.set_center_freq(self.offset+self.fine+self.xfine)

	def get_volume(self):
		return self.volume

	def set_volume(self, volume):
		self.volume = volume
		self.gr_multiply_const_vxx_1.set_k((0.0 if self.muted else self.volume/4.5, ))
		self._volume_slider.set_value(self.volume)
		self._volume_text_box.set_value(self.volume)

	def get_variable_static_text_1(self):
		return self.variable_static_text_1

	def set_variable_static_text_1(self, variable_static_text_1):
		self.variable_static_text_1 = variable_static_text_1
		self._variable_static_text_1_static_text.set_value(self.variable_static_text_1)

	def get_variable_static_text_0(self):
		return self.variable_static_text_0

	def set_variable_static_text_0(self, variable_static_text_0):
		self.variable_static_text_0 = variable_static_text_0
		self._variable_static_text_0_static_text.set_value(self.variable_static_text_0)

	def get_upc_offset(self):
		return self.upc_offset

	def set_upc_offset(self, upc_offset):
		self.upc_offset = upc_offset
		self.osmosdr_source_c_0.set_center_freq(self.cur_freq+self.offset+(self.upc_offset*float(self.upc)), 0)
		self._upc_offset_text_box.set_value(self.upc_offset)

	def get_upc(self):
		return self.upc

	def set_upc(self, upc):
		self.upc = upc
		self.osmosdr_source_c_0.set_center_freq(self.cur_freq+self.offset+(self.upc_offset*float(self.upc)), 0)
		self._upc_check_box.set_value(self.upc)

	def get_ssb_modes(self):
		return self.ssb_modes

	def set_ssb_modes(self, ssb_modes):
		self.ssb_modes = ssb_modes
		self.gr_multiply_const_vxx_0_0.set_k((1.25 if self.mode in self.ssb_modes else 0.0, ))

	def get_sc_list_len(self):
		return self.sc_list_len

	def set_sc_list_len(self, sc_list_len):
		self.sc_list_len = sc_list_len

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.osmosdr_source_c_0.set_sample_rate(self.samp_rate)
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
		self.gr_fractional_interpolator_xx_1.set_interp_ratio((self.samp_rate/4)/self.wbfm)
		self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 98e3, 55e3, firdes.WIN_HAMMING, 6.76))

	def get_rfgain(self):
		return self.rfgain

	def set_rfgain(self, rfgain):
		self.rfgain = rfgain
		self.osmosdr_source_c_0.set_gain(25 if self.iagc == 1 else self.rfgain, 0)
		self._rfgain_slider.set_value(self.rfgain)
		self._rfgain_text_box.set_value(self.rfgain)

	def get_record_file(self):
		return self.record_file

	def set_record_file(self, record_file):
		self.record_file = record_file
		self.gr_wavfile_sink_0.open("/dev/null" if self.record == False else self.record_file)
		self._record_file_text_box.set_value(self.record_file)

	def get_record(self):
		return self.record

	def set_record(self, record):
		self.record = record
		self.gr_wavfile_sink_0.open("/dev/null" if self.record == False else self.record_file)
		self._record_check_box.set_value(self.record)

	def get_offset(self):
		return self.offset

	def set_offset(self, offset):
		self.offset = offset
		self.osmosdr_source_c_0.set_center_freq(self.cur_freq+self.offset+(self.upc_offset*float(self.upc)), 0)
		self._offset_slider.set_value(self.offset)
		self._offset_text_box.set_value(self.offset)
		self.gr_freq_xlating_fir_filter_xxx_0_1.set_center_freq(self.offset+self.fine+self.xfine)

	def get_muted(self):
		return self.muted

	def set_muted(self, muted):
		self.muted = muted
		self.gr_multiply_const_vxx_1.set_k((0.0 if self.muted else self.volume/4.5, ))

	def get_k(self):
		return self.k

	def set_k(self, k):
		self.k = k
		self.gr_quadrature_demod_cf_0.set_gain(self.k)

	def get_iagc(self):
		return self.iagc

	def set_iagc(self, iagc):
		self.iagc = iagc
		self.osmosdr_source_c_0.set_gain_mode(self.iagc, 0)
		self.osmosdr_source_c_0.set_gain(25 if self.iagc == 1 else self.rfgain, 0)
		self._iagc_check_box.set_value(self.iagc)

	def get_freq_update(self):
		return self.freq_update

	def set_freq_update(self, freq_update):
		self.freq_update = freq_update
		self.wxgui_fftsink2_0.set_baseband_freq(mh.get_last_returned(self.freq_update))
		self.wxgui_waterfallsink2_0.set_baseband_freq(mh.get_last_returned(self.freq_update))

	def get_fm_modes(self):
		return self.fm_modes

	def set_fm_modes(self, fm_modes):
		self.fm_modes = fm_modes
		self.gr_multiply_const_vxx_2.set_k((1.0 if self.mode in self.fm_modes else 0.0, ))

	def get_fm_mode_labels(self):
		return self.fm_mode_labels

	def set_fm_mode_labels(self, fm_mode_labels):
		self.fm_mode_labels = fm_mode_labels

	def get_fine(self):
		return self.fine

	def set_fine(self, fine):
		self.fine = fine
		self._fine_slider.set_value(self.fine)
		self._fine_text_box.set_value(self.fine)
		self.gr_freq_xlating_fir_filter_xxx_0_1.set_center_freq(self.offset+self.fine+self.xfine)

	def get_audio_int_rate(self):
		return self.audio_int_rate

	def set_audio_int_rate(self, audio_int_rate):
		self.audio_int_rate = audio_int_rate
		self.gr_fractional_interpolator_xx_0.set_interp_ratio(self.audio_int_rate/self.arate)
		self.wxgui_waterfallsink2_0_0.set_sample_rate(self.audio_int_rate)
		self.gr_keep_one_in_n_0.set_n(int(self.wbfm/self.audio_int_rate))
		self.band_pass_filter_1.set_taps(firdes.band_pass(1.25, self.audio_int_rate, 100, 6.0e3, 2.5e3, firdes.WIN_HAMMING, 6.76))
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1.0, self.audio_int_rate, self.am_filt_dict_low[self.mode], self.am_filt_dict_high[self.mode], self.bw/2.5, firdes.WIN_HAMMING, 6.76))

	def get_am_modes(self):
		return self.am_modes

	def set_am_modes(self, am_modes):
		self.am_modes = am_modes
		self.gr_multiply_const_vxx_0_0_0.set_k((1.0 if self.mode in self.am_modes else 0.0, ))

	def get_am_filt_dict_low(self):
		return self.am_filt_dict_low

	def set_am_filt_dict_low(self, am_filt_dict_low):
		self.am_filt_dict_low = am_filt_dict_low
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1.0, self.audio_int_rate, self.am_filt_dict_low[self.mode], self.am_filt_dict_high[self.mode], self.bw/2.5, firdes.WIN_HAMMING, 6.76))

	def get_am_filt_dict_high(self):
		return self.am_filt_dict_high

	def set_am_filt_dict_high(self, am_filt_dict_high):
		self.am_filt_dict_high = am_filt_dict_high
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1.0, self.audio_int_rate, self.am_filt_dict_low[self.mode], self.am_filt_dict_high[self.mode], self.bw/2.5, firdes.WIN_HAMMING, 6.76))

	def get_adjusted(self):
		return self.adjusted

	def set_adjusted(self, adjusted):
		self.adjusted = adjusted

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--ahw", dest="ahw", type="string", default="default",
		help="Set Audio Hardware [default=%default]")
	parser.add_option("", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(150.0e6),
		help="Set Center Frequency [default=%default]")
	parser.add_option("", "--ppm", dest="ppm", type="eng_float", default=eng_notation.num_to_str(0.0),
		help="Set PPM Error [default=%default]")
	parser.add_option("", "--vol", dest="vol", type="eng_float", default=eng_notation.num_to_str(1.0),
		help="Set Volume [default=%default]")
	parser.add_option("", "--ftune", dest="ftune", type="eng_float", default=eng_notation.num_to_str(0.0),
		help="Set Fine Tuning [default=%default]")
	parser.add_option("", "--xftune", dest="xftune", type="eng_float", default=eng_notation.num_to_str(0.0),
		help="Set Extra Fine Tuning [default=%default]")
	parser.add_option("", "--srate", dest="srate", type="eng_float", default=eng_notation.num_to_str(1.0e6),
		help="Set RF Sample Rate [default=%default]")
	parser.add_option("", "--upclo", dest="upclo", type="eng_float", default=eng_notation.num_to_str(0.0),
		help="Set Upconverter LO Frequency [default=%default]")
	parser.add_option("", "--devinfo", dest="devinfo", type="string", default="rtl=0",
		help="Set Device Information [default=%default]")
	parser.add_option("", "--agc", dest="agc", type="intx", default=0,
		help="Set AGC On/Off [default=%default]")
	parser.add_option("", "--arate", dest="arate", type="eng_float", default=eng_notation.num_to_str(48.0e3),
		help="Set Audio Sample Rate [default=%default]")
	parser.add_option("", "--upce", dest="upce", type="intx", default=0,
		help="Set Upconverter Enabled [default=%default]")
	parser.add_option("", "--mbw", dest="mbw", type="eng_float", default=eng_notation.num_to_str(2.0e3),
		help="Set AM/SSB Demod Bandwidth [default=%default]")
	parser.add_option("", "--mthresh", dest="mthresh", type="eng_float", default=eng_notation.num_to_str(-10.0),
		help="Set Mute Threshold (dB) [default=%default]")
	parser.add_option("", "--flist", dest="flist", type="string", default="",
		help="Set Frequency Scan List [default=%default]")
	parser.add_option("", "--dmode", dest="dmode", type="string", default="NFM1",
		help="Set Demod Mode [default=%default]")
	parser.add_option("", "--offs", dest="offs", type="eng_float", default=eng_notation.num_to_str(50.e3),
		help="Set LO Offset [default=%default]")
	(options, args) = parser.parse_args()
	tb = multimode(ahw=options.ahw, freq=options.freq, ppm=options.ppm, vol=options.vol, ftune=options.ftune, xftune=options.xftune, srate=options.srate, upclo=options.upclo, devinfo=options.devinfo, agc=options.agc, arate=options.arate, upce=options.upce, mbw=options.mbw, mthresh=options.mthresh, flist=options.flist, dmode=options.dmode, offs=options.offs)
	tb.Run(True, 350)

