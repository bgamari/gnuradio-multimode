#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Multimode
# Generated: Mon May 21 14:45:33 2012
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
import osmosdr
import threading
import time
import wx

class multimode(grc_wxgui.top_block_gui):

	def __init__(self, devinfo="rtl=0", ahw="default", freq=150.0e6, ppm=0.0, vol=1.0, ftune=0.0, xftune=0.0, offs=50.e3, mbw=2.0e3, dmode='FM', mthresh=-10.0, arate=48.0e3, srate=1.0e6, agc=0):
		grc_wxgui.top_block_gui.__init__(self, title="Multimode")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.devinfo = devinfo
		self.ahw = ahw
		self.freq = freq
		self.ppm = ppm
		self.vol = vol
		self.ftune = ftune
		self.xftune = xftune
		self.offs = offs
		self.mbw = mbw
		self.dmode = dmode
		self.mthresh = mthresh
		self.arate = arate
		self.srate = srate
		self.agc = agc

		##################################################
		# Variables
		##################################################
		self.wbfm = wbfm = 200e3
		self.rf_power = rf_power = 0
		self.thresh = thresh = mthresh
		self.samp_rate = samp_rate = int(int(srate/wbfm)*wbfm)
		self.quad_rate = quad_rate = wbfm
		self.mode = mode = dmode
		self.logpower = logpower = math.log10(rf_power+1.0e-12)*10.0
		self.deviation_dict = deviation_dict = {'FM' : 7.5e3, 'WFM' : 95e3, 'TV-FM' : 25e3, 'AM' : 5.5e3, 'USB' : 5.5e3, 'LSB' : 5.5e3}
		self.adjusted = adjusted = "" if int(srate) % int(wbfm) == 0 else " (adjusted from "+str(srate/1.0e6)+"Msps)"
		self.xfine = xfine = xftune
		self.volume = volume = vol
		self.variable_static_text_1_0 = variable_static_text_1_0 = devinfo
		self.variable_static_text_1 = variable_static_text_1 = str(samp_rate/1.0e6)+"Msps"+adjusted
		self.variable_static_text_0 = variable_static_text_0 = float(int(math.log10(rf_power+1.0e-14)*100.0)/10.0)
		self.rfgain = rfgain = 25
		self.record_file = record_file = "recording.wav"
		self.record = record = False
		self.offset = offset = offs
		self.muted = muted = 0.0 if logpower >= thresh else 1
		self.k = k = quad_rate/(2*math.pi*deviation_dict[mode])
		self.ifreq = ifreq = freq
		self.iagc = iagc = agc
		self.fine = fine = ftune
		self.bw = bw = mbw
		self.audio_int_rate = audio_int_rate = 25e3

		##################################################
		# Blocks
		##################################################
		_xfine_sizer = wx.BoxSizer(wx.VERTICAL)
		self._xfine_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_xfine_sizer,
			value=self.xfine,
			callback=self.set_xfine,
			label="Extra Fine Tuning",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._xfine_slider = forms.slider(
			parent=self.GetWin(),
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
		self.GridAdd(_xfine_sizer, 0, 3, 1, 1)
		_volume_sizer = wx.BoxSizer(wx.VERTICAL)
		self._volume_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_volume_sizer,
			value=self.volume,
			callback=self.set_volume,
			label="Volume",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._volume_slider = forms.slider(
			parent=self.GetWin(),
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
		self.GridAdd(_volume_sizer, 0, 0, 1, 1)
		_rfgain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._rfgain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_rfgain_sizer,
			value=self.rfgain,
			callback=self.set_rfgain,
			label="RF Gain",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._rfgain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_rfgain_sizer,
			value=self.rfgain,
			callback=self.set_rfgain,
			minimum=0,
			maximum=40,
			num_steps=200,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_rfgain_sizer, 2, 1, 1, 1)
		self.rf_probe = gr.probe_avg_mag_sqrd_c(0, 1.0/(samp_rate/50.0))
		self._record_file_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.record_file,
			callback=self.set_record_file,
			label="Recording Filename",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._record_file_text_box, 2, 4, 1, 1)
		self._record_check_box = forms.check_box(
			parent=self.GetWin(),
			value=self.record,
			callback=self.set_record,
			label="Record",
			true=True,
			false=False,
		)
		self.GridAdd(self._record_check_box, 2, 3, 1, 1)
		_offset_sizer = wx.BoxSizer(wx.VERTICAL)
		self._offset_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_offset_sizer,
			value=self.offset,
			callback=self.set_offset,
			label="LO Offset",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._offset_slider = forms.slider(
			parent=self.GetWin(),
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
		self.GridAdd(_offset_sizer, 1, 3, 1, 1)
		self._mode_chooser = forms.radio_buttons(
			parent=self.GetWin(),
			value=self.mode,
			callback=self.set_mode,
			label="Mode",
			choices=['FM','AM','USB','LSB','WFM','TV-FM'],
			labels=[],
			style=wx.RA_HORIZONTAL,
		)
		self.GridAdd(self._mode_chooser, 0, 4, 1, 1)
		self._ifreq_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.ifreq,
			callback=self.set_ifreq,
			label="Frequency",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._ifreq_text_box, 0, 1, 1, 1)
		self._iagc_check_box = forms.check_box(
			parent=self.GetWin(),
			value=self.iagc,
			callback=self.set_iagc,
			label="AGC",
			true=1,
			false=0,
		)
		self.GridAdd(self._iagc_check_box, 2, 0, 1, 1)
		_fine_sizer = wx.BoxSizer(wx.VERTICAL)
		self._fine_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_fine_sizer,
			value=self.fine,
			callback=self.set_fine,
			label="Fine Tuning",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._fine_slider = forms.slider(
			parent=self.GetWin(),
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
		self.GridAdd(_fine_sizer, 0, 2, 1, 1)
		_bw_sizer = wx.BoxSizer(wx.VERTICAL)
		self._bw_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_bw_sizer,
			value=self.bw,
			callback=self.set_bw,
			label="AM/SSB Bandwidth",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._bw_slider = forms.slider(
			parent=self.GetWin(),
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
		self.GridAdd(_bw_sizer, 1, 2, 1, 1)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.GetWin(),
			baseband_freq=ifreq,
			dynamic_range=40,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=5,
			average=True,
			avg_alpha=None,
			title="Spectrogram",
			win=window.hamming,
		)
		self.Add(self.wxgui_waterfallsink2_0.win)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=ifreq,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=8,
			average=True,
			avg_alpha=0.1,
			title="Panorama",
			peak_hold=False,
			win=window.hamming,
		)
		self.Add(self.wxgui_fftsink2_0.win)
		self._variable_static_text_1_0_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.variable_static_text_1_0,
			callback=self.set_variable_static_text_1_0,
			label="Devinfo",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._variable_static_text_1_0_static_text, 3, 0, 1, 3)
		self._variable_static_text_1_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.variable_static_text_1,
			callback=self.set_variable_static_text_1,
			label="Sample Rate",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._variable_static_text_1_static_text, 2, 2, 1, 1)
		self._variable_static_text_0_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.variable_static_text_0,
			callback=self.set_variable_static_text_0,
			label="RF Level",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._variable_static_text_0_static_text, 1, 0, 1, 1)
		_thresh_sizer = wx.BoxSizer(wx.VERTICAL)
		self._thresh_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_thresh_sizer,
			value=self.thresh,
			callback=self.set_thresh,
			label="Mute Threshold",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._thresh_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_thresh_sizer,
			value=self.thresh,
			callback=self.set_thresh,
			minimum=-40,
			maximum=10,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_thresh_sizer, 1, 1, 1, 1)
		def _rf_power_probe():
			while True:
				val = self.rf_probe.level()
				try: self.set_rf_power(val)
				except AttributeError, e: pass
				time.sleep(1.0/(10))
		_rf_power_thread = threading.Thread(target=_rf_power_probe)
		_rf_power_thread.daemon = True
		_rf_power_thread.start()
		self.osmosdr_source_c_0 = osmosdr.source_c( args="nchan=" + str(1) + " " + devinfo  )
		self.osmosdr_source_c_0.set_sample_rate(samp_rate)
		self.osmosdr_source_c_0.set_center_freq(ifreq+offset, 0)
		self.osmosdr_source_c_0.set_freq_corr(ppm, 0)
		self.osmosdr_source_c_0.set_gain_mode(iagc, 0)
		self.osmosdr_source_c_0.set_gain(25 if iagc == 1 else rfgain, 0)
		self.low_pass_filter_4 = gr.fir_filter_fff(1, firdes.low_pass(
			2.5, audio_int_rate, 5.0e3, 2.0e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_3 = gr.fir_filter_ccf(int((audio_int_rate*8)/(audio_int_rate)), firdes.low_pass(
			1, audio_int_rate*8, 11.5e3, 7.5e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_2 = gr.fir_filter_fff(int(quad_rate/audio_int_rate), firdes.low_pass(
			1, wbfm, 15e3, 4e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_1_0 = gr.fir_filter_ccf(1, firdes.low_pass(
			1, audio_int_rate, bw/2.0, bw/3.5, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_1 = gr.fir_filter_ccf(int(samp_rate/wbfm), firdes.low_pass(
			1, samp_rate, 98e3, 55e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0 = gr.fir_filter_ccf(1, firdes.low_pass(
			1, wbfm, deviation_dict[mode], deviation_dict[mode]/3.3, firdes.WIN_HAMMING, 6.76))
		self.gr_wavfile_sink_0 = gr.wavfile_sink("/dev/null" if record == False else record_file, 1, int(audio_int_rate), 8)
		self.gr_quadrature_demod_cf_0 = gr.quadrature_demod_cf(k)
		self.gr_multiply_const_vxx_2 = gr.multiply_const_vff((1.0 if mode == 'WFM' or mode == 'FM' or mode == 'TV-FM' else 0.0, ))
		self.gr_multiply_const_vxx_1 = gr.multiply_const_vff((0.0 if muted else volume/4.5, ))
		self.gr_multiply_const_vxx_0_0_0 = gr.multiply_const_vff((1.0 if mode == 'AM' else 0.0, ))
		self.gr_multiply_const_vxx_0_0 = gr.multiply_const_vff((2.0 if (mode == 'LSB' or mode == 'USB') else 0.0, ))
		self.gr_freq_xlating_fir_filter_xxx_0_1 = gr.freq_xlating_fir_filter_ccc(1, (1.0, ), offset+fine+xfine, samp_rate)
		self.gr_fractional_interpolator_xx_0 = gr.fractional_interpolator_ff(0, audio_int_rate/arate)
		self.gr_feedforward_agc_cc_0 = gr.feedforward_agc_cc(1024, 0.45)
		self.gr_complex_to_real_0 = gr.complex_to_real(1)
		self.gr_complex_to_mag_squared_0 = gr.complex_to_mag_squared(1)
		self.gr_agc2_xx_1 = gr.agc2_cc(1e-1, 1e-2, 0.75, 1.0, 0.0)
		self.gr_add_xx_0 = gr.add_vff(1)
		self.blks2_fm_deemph_0 = blks2.fm_deemph(fs=audio_int_rate, tau=75e-6)
		self.band_pass_filter_0 = gr.fir_filter_ccc(1, firdes.complex_band_pass(
			1, audio_int_rate, -(bw/2) if mode == 'LSB' else 0, 0 if mode == 'LSB' else bw/2, bw/3.5, firdes.WIN_HAMMING, 6.76))
		self.audio_sink_0 = audio.sink(int(arate), ahw, True)

		##################################################
		# Connections
		##################################################
		self.connect((self.band_pass_filter_0, 0), (self.gr_complex_to_real_0, 0))
		self.connect((self.gr_complex_to_real_0, 0), (self.gr_multiply_const_vxx_0_0, 0))
		self.connect((self.gr_multiply_const_vxx_0_0, 0), (self.gr_add_xx_0, 1))
		self.connect((self.gr_fractional_interpolator_xx_0, 0), (self.gr_multiply_const_vxx_1, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0_1, 0), (self.wxgui_waterfallsink2_0, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.audio_sink_0, 1))
		self.connect((self.gr_complex_to_mag_squared_0, 0), (self.low_pass_filter_4, 0))
		self.connect((self.low_pass_filter_4, 0), (self.gr_multiply_const_vxx_0_0_0, 0))
		self.connect((self.gr_add_xx_0, 0), (self.gr_fractional_interpolator_xx_0, 0))
		self.connect((self.gr_add_xx_0, 0), (self.gr_wavfile_sink_0, 0))
		self.connect((self.low_pass_filter_1_0, 0), (self.gr_feedforward_agc_cc_0, 0))
		self.connect((self.gr_feedforward_agc_cc_0, 0), (self.band_pass_filter_0, 0))
		self.connect((self.gr_feedforward_agc_cc_0, 0), (self.gr_complex_to_mag_squared_0, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0_1, 0))
		self.connect((self.gr_agc2_xx_1, 0), (self.low_pass_filter_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.gr_quadrature_demod_cf_0, 0))
		self.connect((self.gr_quadrature_demod_cf_0, 0), (self.low_pass_filter_2, 0))
		self.connect((self.low_pass_filter_2, 0), (self.blks2_fm_deemph_0, 0))
		self.connect((self.blks2_fm_deemph_0, 0), (self.gr_multiply_const_vxx_2, 0))
		self.connect((self.gr_multiply_const_vxx_0_0_0, 0), (self.gr_add_xx_0, 2))
		self.connect((self.gr_multiply_const_vxx_2, 0), (self.gr_add_xx_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0_1, 0), (self.low_pass_filter_1, 0))
		self.connect((self.low_pass_filter_1, 0), (self.gr_agc2_xx_1, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0_1, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.low_pass_filter_3, 0), (self.low_pass_filter_1_0, 0))
		self.connect((self.low_pass_filter_1, 0), (self.low_pass_filter_3, 0))
		self.connect((self.low_pass_filter_1, 0), (self.rf_probe, 0))

	def get_devinfo(self):
		return self.devinfo

	def set_devinfo(self, devinfo):
		self.devinfo = devinfo
		self.set_variable_static_text_1_0(self.devinfo)

	def get_ahw(self):
		return self.ahw

	def set_ahw(self, ahw):
		self.ahw = ahw

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
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

	def get_offs(self):
		return self.offs

	def set_offs(self, offs):
		self.offs = offs
		self.set_offset(self.offs)

	def get_mbw(self):
		return self.mbw

	def set_mbw(self, mbw):
		self.mbw = mbw
		self.set_bw(self.mbw)

	def get_dmode(self):
		return self.dmode

	def set_dmode(self, dmode):
		self.dmode = dmode
		self.set_mode(self.dmode)

	def get_mthresh(self):
		return self.mthresh

	def set_mthresh(self, mthresh):
		self.mthresh = mthresh
		self.set_thresh(self.mthresh)

	def get_arate(self):
		return self.arate

	def set_arate(self, arate):
		self.arate = arate
		self.gr_fractional_interpolator_xx_0.set_interp_ratio(self.audio_int_rate/self.arate)

	def get_srate(self):
		return self.srate

	def set_srate(self, srate):
		self.srate = srate
		self.set_samp_rate(int(int(self.srate/self.wbfm)*self.wbfm))
		self.set_adjusted("" if int(self.srate) % int(self.wbfm) == 0 else " (adjusted from "+str(self.srate/1.0e6)+"Msps)")

	def get_agc(self):
		return self.agc

	def set_agc(self, agc):
		self.agc = agc
		self.set_iagc(self.agc)

	def get_wbfm(self):
		return self.wbfm

	def set_wbfm(self, wbfm):
		self.wbfm = wbfm
		self.set_samp_rate(int(int(self.srate/self.wbfm)*self.wbfm))
		self.set_adjusted("" if int(self.srate) % int(self.wbfm) == 0 else " (adjusted from "+str(self.srate/1.0e6)+"Msps)")
		self.low_pass_filter_2.set_taps(firdes.low_pass(1, self.wbfm, 15e3, 4e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wbfm, self.deviation_dict[self.mode], self.deviation_dict[self.mode]/3.3, firdes.WIN_HAMMING, 6.76))
		self.set_quad_rate(self.wbfm)

	def get_rf_power(self):
		return self.rf_power

	def set_rf_power(self, rf_power):
		self.rf_power = rf_power
		self.set_variable_static_text_0(float(int(math.log10(self.rf_power+1.0e-14)*100.0)/10.0))
		self.set_logpower(math.log10(self.rf_power+1.0e-12)*10.0)

	def get_thresh(self):
		return self.thresh

	def set_thresh(self, thresh):
		self.thresh = thresh
		self._thresh_slider.set_value(self.thresh)
		self._thresh_text_box.set_value(self.thresh)
		self.set_muted(0.0 if self.logpower >= self.thresh else 1)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 98e3, 55e3, firdes.WIN_HAMMING, 6.76))
		self.rf_probe.set_alpha(1.0/(self.samp_rate/50.0))
		self.set_variable_static_text_1(str(self.samp_rate/1.0e6)+"Msps"+self.adjusted)
		self.osmosdr_source_c_0.set_sample_rate(self.samp_rate)
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

	def get_quad_rate(self):
		return self.quad_rate

	def set_quad_rate(self, quad_rate):
		self.quad_rate = quad_rate
		self.set_k(self.quad_rate/(2*math.pi*self.deviation_dict[self.mode]))

	def get_mode(self):
		return self.mode

	def set_mode(self, mode):
		self.mode = mode
		self.gr_multiply_const_vxx_0_0.set_k((2.0 if (self.mode == 'LSB' or self.mode == 'USB') else 0.0, ))
		self.set_k(self.quad_rate/(2*math.pi*self.deviation_dict[self.mode]))
		self.gr_multiply_const_vxx_0_0_0.set_k((1.0 if self.mode == 'AM' else 0.0, ))
		self.gr_multiply_const_vxx_2.set_k((1.0 if self.mode == 'WFM' or self.mode == 'FM' or self.mode == 'TV-FM' else 0.0, ))
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_int_rate, -(self.bw/2) if self.mode == 'LSB' else 0, 0 if self.mode == 'LSB' else self.bw/2, self.bw/3.5, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wbfm, self.deviation_dict[self.mode], self.deviation_dict[self.mode]/3.3, firdes.WIN_HAMMING, 6.76))
		self._mode_chooser.set_value(self.mode)

	def get_logpower(self):
		return self.logpower

	def set_logpower(self, logpower):
		self.logpower = logpower
		self.set_muted(0.0 if self.logpower >= self.thresh else 1)

	def get_deviation_dict(self):
		return self.deviation_dict

	def set_deviation_dict(self, deviation_dict):
		self.deviation_dict = deviation_dict
		self.set_k(self.quad_rate/(2*math.pi*self.deviation_dict[self.mode]))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wbfm, self.deviation_dict[self.mode], self.deviation_dict[self.mode]/3.3, firdes.WIN_HAMMING, 6.76))

	def get_adjusted(self):
		return self.adjusted

	def set_adjusted(self, adjusted):
		self.adjusted = adjusted
		self.set_variable_static_text_1(str(self.samp_rate/1.0e6)+"Msps"+self.adjusted)

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

	def get_variable_static_text_1_0(self):
		return self.variable_static_text_1_0

	def set_variable_static_text_1_0(self, variable_static_text_1_0):
		self.variable_static_text_1_0 = variable_static_text_1_0
		self._variable_static_text_1_0_static_text.set_value(self.variable_static_text_1_0)

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

	def get_rfgain(self):
		return self.rfgain

	def set_rfgain(self, rfgain):
		self.rfgain = rfgain
		self._rfgain_slider.set_value(self.rfgain)
		self._rfgain_text_box.set_value(self.rfgain)
		self.osmosdr_source_c_0.set_gain(25 if self.iagc == 1 else self.rfgain, 0)

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
		self._offset_slider.set_value(self.offset)
		self._offset_text_box.set_value(self.offset)
		self.gr_freq_xlating_fir_filter_xxx_0_1.set_center_freq(self.offset+self.fine+self.xfine)
		self.osmosdr_source_c_0.set_center_freq(self.ifreq+self.offset, 0)

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

	def get_ifreq(self):
		return self.ifreq

	def set_ifreq(self, ifreq):
		self.ifreq = ifreq
		self._ifreq_text_box.set_value(self.ifreq)
		self.osmosdr_source_c_0.set_center_freq(self.ifreq+self.offset, 0)
		self.wxgui_fftsink2_0.set_baseband_freq(self.ifreq)
		self.wxgui_waterfallsink2_0.set_baseband_freq(self.ifreq)

	def get_iagc(self):
		return self.iagc

	def set_iagc(self, iagc):
		self.iagc = iagc
		self._iagc_check_box.set_value(self.iagc)
		self.osmosdr_source_c_0.set_gain_mode(self.iagc, 0)
		self.osmosdr_source_c_0.set_gain(25 if self.iagc == 1 else self.rfgain, 0)

	def get_fine(self):
		return self.fine

	def set_fine(self, fine):
		self.fine = fine
		self._fine_slider.set_value(self.fine)
		self._fine_text_box.set_value(self.fine)
		self.gr_freq_xlating_fir_filter_xxx_0_1.set_center_freq(self.offset+self.fine+self.xfine)

	def get_bw(self):
		return self.bw

	def set_bw(self, bw):
		self.bw = bw
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_int_rate, -(self.bw/2) if self.mode == 'LSB' else 0, 0 if self.mode == 'LSB' else self.bw/2, self.bw/3.5, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, self.audio_int_rate, self.bw/2.0, self.bw/3.5, firdes.WIN_HAMMING, 6.76))
		self._bw_slider.set_value(self.bw)
		self._bw_text_box.set_value(self.bw)

	def get_audio_int_rate(self):
		return self.audio_int_rate

	def set_audio_int_rate(self, audio_int_rate):
		self.audio_int_rate = audio_int_rate
		self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_int_rate, -(self.bw/2) if self.mode == 'LSB' else 0, 0 if self.mode == 'LSB' else self.bw/2, self.bw/3.5, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_3.set_taps(firdes.low_pass(1, self.audio_int_rate*8, 11.5e3, 7.5e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_4.set_taps(firdes.low_pass(2.5, self.audio_int_rate, 5.0e3, 2.0e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, self.audio_int_rate, self.bw/2.0, self.bw/3.5, firdes.WIN_HAMMING, 6.76))
		self.gr_fractional_interpolator_xx_0.set_interp_ratio(self.audio_int_rate/self.arate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--devinfo", dest="devinfo", type="string", default="rtl=0",
		help="Set Device Information [default=%default]")
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
	parser.add_option("", "--offs", dest="offs", type="eng_float", default=eng_notation.num_to_str(50.e3),
		help="Set LO Offset [default=%default]")
	parser.add_option("", "--mbw", dest="mbw", type="eng_float", default=eng_notation.num_to_str(2.0e3),
		help="Set AM/SSB Demod Bandwidth [default=%default]")
	parser.add_option("", "--dmode", dest="dmode", type="string", default='FM',
		help="Set Demod Mode [default=%default]")
	parser.add_option("", "--mthresh", dest="mthresh", type="eng_float", default=eng_notation.num_to_str(-10.0),
		help="Set Mute Threshold (dB) [default=%default]")
	parser.add_option("", "--arate", dest="arate", type="eng_float", default=eng_notation.num_to_str(48.0e3),
		help="Set Audio Sample Rate [default=%default]")
	parser.add_option("", "--srate", dest="srate", type="eng_float", default=eng_notation.num_to_str(1.0e6),
		help="Set RF Sample Rate [default=%default]")
	parser.add_option("", "--agc", dest="agc", type="intx", default=0,
		help="Set AGC On/Off [default=%default]")
	(options, args) = parser.parse_args()
	tb = multimode(devinfo=options.devinfo, ahw=options.ahw, freq=options.freq, ppm=options.ppm, vol=options.vol, ftune=options.ftune, xftune=options.xftune, offs=options.offs, mbw=options.mbw, dmode=options.dmode, mthresh=options.mthresh, arate=options.arate, srate=options.srate, agc=options.agc)
	tb.Run(True)

