# This is an Ishmael settings file.  It is okay to edit it with a text
# editor or word processor, provided you save it as TEXT ONLY.  It's
# generally safe to change the values here in ways that seem reasonable,
# though you could undoubtedly make Ishmael fail with some really poor
# choices of values.
# 
# Also:
#    * Keep each line in its original section (Unit) or it will be ignored.
#
#    * A line beginning with '#', like this one, is a comment.
#
#    * Spaces and capitalization in parameter names ARE significant.
#
#    * If you delete a line containing a certain parameter, then loading
#      this settings file will not affect Ishmael's current value of that
#      parameter.  So you can create a settings file with only a handful of
#      lines for your favorite values, and when you load that file, it will
#      set those parameters and leave everything else alone.
#
#    * When you save settings, beware that ALL parameter values are written
#      out, not just the ones you may have set in your parameters file.
#
#    * Ishmael's default settings file -- the one it loads at startup -- is
#      called IshDefault.ipf .


Unit: Sound file I/O, prefs version 1
    time zone offset     = -28800
    name template        = test%f_%y%M%D-%H%m%s.wav
    binread sample rate  = 44100.000000
    binread #channels    = 1
    binread bytes/sample = 2
    binread float samples = false
    binread ignore start = 0
    binread ignore end   = 0
    binread win byteorder = true
    binread ask unrecognized = false
    binread recog template = *.myExten
    binread name hack    = C:\Ishmael 0.9\bin\foo.i16win
    binwrite bytes/sample = 2
    binwrite float samples = false
    binwrite win byteorder = true
    binwrite name hack   = *.i16win
    binread sample offset = 0.000000

Unit: Sound card I/O, prefs version 1
    input active         = false
    in device ID         = 0
    sample rate          = 22050.000000
    in channels enabled  = 1000000000000000
    out device ID        = 0
    out speedup          = 1
    out chan left        = 0
    out chan right       = 0
    unprepare buffers    = false
    playback looping     = false

Unit: ASIO device input, prefs version 1
    input active         = false
    in device ID         = 0
    sample rate          = 11025.000000
    in channels enabled  = 1100000000000000
    input gain           = -96

Unit: File input, prefs version 1
    active               = true
    file name            = C:\Users\BIOWAVES\PycharmProjects\audioMerger\test\Multichannel_Output\M-170813-153500.wav
    enabled channels     = 1111000000000000000000000000000000000000000000000000000000000000
    pause after each file = false
    fit file to window T = true
    fit file to window F = false
    time source          = 1
    time template        = %2y%2M%2D_%2h%2m%2s.aif
    explicit date        = 1/1/2000
    explicit time        = 9:00:00
    time zone seconds    = 0
    file start time      = 0.000000
    play rate factor     = +INF
    autorun on startup   = false
    batch file names     = C:\Users\BIOWAVES\PycharmProjects\audioMerger\test\Multichannel_Output\M-170813-153500.wav

Unit: Splitter, prefs version 1
    number of subsystems = 0

Unit: Filter Calculation, prefs version 1
    filter parameter array, size = 0
    filter parameter array end = end of array

Unit: Sound recording, prefs version 2
    recording on?        = 0
    max file length      = 600.000000
    time align files     = true
    record only realtime = true
    directory            = C:\Users\PODS Staff\Desktop\2013 PODS Cruise\Array Recordings 2013\END ARRAY_HP1_HP5
    sampling enabled     = false
    sampling cycle time  = 10.000000
    sampling start time  = 2.000000
    sampling stop time   = 7.000000
    time align sampling  = false
    pre-click time       = 0
    log recorded file names = false

Unit: Spectrogram calculation, prefs version 1
    frame size, samples  = 1024
    frame size, sec      = 0.081919998
    zero pad             = 0
    hop size             = 512
    window type          = Hamming
    keep same duration   = true
    quadratic scaling    = false

Unit: Equalization, prefs version 1
    equalization enabled = false
    equalization time    = 60
    floor enabled        = true
    floor is automatic   = false
    gram floor value     = 0.30399999
    ceiling enabled      = false
    ceiling is automatic = true
    gram ceiling value   = 4.1773291

Unit: Energy sum, prefs version 1
    enabled              = false
    lower frequency bound = 50
    upper frequency bound = 200
    ratio enabled        = false
    ratio lower freq bound = 1000
    ratio upper freq bound = 2000

Unit: Tonal detection 1, prefs version 1
    enabled              = false
    lower frequency bound = 1000
    upper frequency bound = 2000
    base percentage      = 50
    height above base    = 1
    peak neighborhood    = 100
    peak min difference  = 100
    line fit duration    = 0.050000001
    minimum duration     = 0.2
    minimum independent dur = 0.1

Unit: Spectrogram correlator, prefs version 1
    enabled              = false
    kernel               = %   t0     t1     f0        f1^015^012     0    12.77  50.67     47.59^015^012
    kernel bandwidth     = 3

Unit: Matched filter, prefs version 1
    enabled              = false
    filter file name     = 
    min detected freq    = 0
    max detected freq    = +INF

Unit: Sequence recognition, prefs version 1
    sumautocorr enabled  = false
    sac window length    = 200
    sac hop size fraction = 0.1
    sac min period       = 5
    sac max period       = 10
    use old method       = false

Unit: Detector, prefs version 1
    time averaging enabled = true
    time averaging constant = 20
    detection threshold  = 0.1
    min call duration    = 0.1
    max call duration    = 1
    detection neighborhood = 0.2
    detection channels   = 1000000000000000000000000000000000000000000000000000000000000000
    save all channels    = false
    time before call     = 60
    time after call      = 60
    retrigger            = false
    display amplitude min = -0.0069726286
    display amplitude max = 0.1587555
    old nbd method       = false
    use system clock     = false
    which time stamp     = 2
    Teager-Kaiser enabled = true

Unit: Spectrogram display, prefs version 1
    display enabled      = true
    tickmark font name   = Arial
    tickmark font size   = 10
    tickmark font bold   = false
    tickmark length      = 5

Unit: Spectrogram display, prefs version 1
    brightness           = 2.1760001
    contrast             = 0.499668
    color map name       = cool
    pause after every screen = false

Unit: Channels displayed, prefs version 1
    channels displayed   = 1111000000000000000000000000000000000000000000000000000000000000

Unit: Display scaling, prefs version 1
    main window position = (-8,-8,1608,868)
    time scaling         = 6.8876061
    time scale preferred = false
    lowest amplitude     = -0.5
    highest amplitude    = 0.5
    amp scale preferred  = false
    lowest frequency     = 0
    highest frequency    = 6000
    freq scale preferred = false

Unit: Time series display, prefs version 1
    display enabled      = true
    tickmark font name   = Arial
    tickmark font size   = 10
    tickmark font bold   = false
    tickmark length      = 5

Unit: Time series display, prefs version 1

Unit: Hyperbolic localization, prefs version 1
    array file name      = C:\Program Files (x86)\Ishmael\Data\LineArray.arr
    speed of sound       = 1484.000000
    pair loc phone 1     = 1
    pair loc phone 2     = 2
    cross pair 1 phone 1 = -1
    cross pair 1 phone 2 = -1
    cross pair 2 phone 1 = 2
    cross pair 2 phone 2 = 3
    disambiguation       = false
    disambig pair phone 1 = -1
    disambig pair phone 2 = -1
    map left edge        = -1000
    map right edge       = 1000
    map top edge         = -1000
    map bottom edge      = 1000
    min Z limit          = -1000
    max Z limit          = 1000
    contour beamforming  = true
    contour strip width  = 1000
    map window position  = (716,351,931,588)
    bearing/time window position = (361,205,834,508)
    xcorr window position = (324,211,754,423)
    serial com port      = 1
    show xcorr display   = 1
    InstaLoc time before = 0.200000
    InstaLoc time after  = 0.200000
    InstaLoc low freq    = 1000
    InstaLoc high freq   = 2000
    InstaLoc loc method  = 0
    reload array file    = false
    log intermediates    = true
    show results         = true
    3-D locations        = false
    propagation medium   = 0
    temperature          = 10.5
    depth                = 100
    salinity             = 35
    show WhaleTrack II messages = false
    get time from WhaleTrack II = false
    send all locs to WhalTrak = false
    send locs to WILD    = false
    WILD UDP port number = 8002
    bearing 0 is X-axis  = false

Unit: Matlab, prefs version 1
    matlab command       = plot(ishSelectionSamples(:,1))
    matlab run dir       = C:\MyHome\MyMatlabDir
    do startup.m         = true

Unit: Time-domain beamforming, prefs version 1
    beamforming enabled  = false
    0 degrees is Y-axis  = true
    beam angles          = 0:45:180
    plot beam angles     = 70
    plot beam freqs      = 500
    weighting enabled    = true

Unit: Data logging, prefs version 1
    msmt name array, size = 37
    msmt name            = start time
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = end time
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = low frequency
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = high frequency
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = user channel
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = duration
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = bandwidth
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = sampling rate
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = spectrogram frame rate
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = time of maximum intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = frequency of maximum intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = maximum intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = centroid frequency
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = centroid time
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = median time
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = temporal interquartile range
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = temporal concentration
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = temporal asymmetry
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = median frequency
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = spectral interquartile range
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = spectral concentration
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = spectral asymmetry
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = time of peak cell intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = relative time of peak cell intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = time of peak overall intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = relative time of peak overall intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = frequency of peak cell intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = frequency of peak overall intensity
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = amplitude modulation rate
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = variation in AM rate
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = frequency modulation rate
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = variation in FM rate
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = average cepstrum peak width
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = overall entropy
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = upsweep mean
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = upsweep fraction
    msmt enabled         = true
    msmt array end       = end of array element
    msmt name            = signal-to-noise ratio
    msmt enabled         = true
    msmt array end       = end of array

Unit: Actions and logging, prefs version 1
    log file enabled     = true
    log file name        = C:\Users\BIOWAVES\PycharmProjects\audioMerger\dir\ish_log.txt
    log comment date     = false
    action array, size   = 3
    ac name              = Call detected
    ac log name          = true
    ac key               = 
    ac log input name    = true
    ac log outfile       = true
    ac log track         = false
    ac log sel T/F       = true
    ac log key           = false
    ac log peak          = true
    ac log comment       = false
    ac comment           = 
    ac next file         = false
    ac save sel          = true
    ac save dir          = K:\DATA\HARP Data\HAT01A\df20\Minke_Pulse_Test\Ishmael Testing
    ac unpause           = false
    ac send Matlab cmd   = false
    ac beamform locate   = false
    ac phone-pair locate = false
    ac hyperbolic locate = false
    ac crossed-pair locate = false
    action array end     = end of array element
    ac name              = Hyperbolic
    ac log name          = true
    ac key               = H
    ac log input name    = true
    ac log outfile       = false
    ac log track         = false
    ac log sel T/F       = true
    ac log key           = false
    ac log peak          = false
    ac log comment       = false
    ac comment           = 
    ac next file         = false
    ac save sel          = false
    ac save dir          = C:\Program Files (x86)\Ishmael\Ishmael 2.4
    ac unpause           = false
    ac send Matlab cmd   = false
    ac beamform locate   = false
    ac phone-pair locate = false
    ac hyperbolic locate = false
    ac crossed-pair locate = false
    action array end     = end of array element
    ac name              = hyperbolicLocPosition
    ac log name          = true
    ac key               = L
    ac log input name    = false
    ac log outfile       = true
    ac log track         = false
    ac log sel T/F       = false
    ac log key           = false
    ac log peak          = false
    ac log comment       = false
    ac comment           = 
    ac next file         = false
    ac save sel          = true
    ac save dir          = C:\Users\BIOWAVES\Desktop\sage
    ac unpause           = false
    ac send Matlab cmd   = false
    ac beamform locate   = false
    ac phone-pair locate = false
    ac hyperbolic locate = true
    ac crossed-pair locate = false
    action array end     = end of array
