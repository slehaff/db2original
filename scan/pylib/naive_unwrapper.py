# Phase unwrapping code, very naive but does the job when there is no noise
# Nazim Bharmal nab26@cantab.net 07/Nov/2012

import numpy as np
import cv2

# Algorithm for unwrapping
# 1. scan line for valid pixels
# 2. if there are valid pixels, break line into contiguous segments
# 3. scan previous line for any pixels which lie under a pixel in the segments
# 4. if there are pixels then use there to establish the vertical phase offset at that pixel
# 5. if there are pixels then unwrap backward to the start of the segement and then forward
# 6. if there aren't pixels then unwrap the segment forwards from the start
# 7. go to the next line
# return to 1


def a_range(x, axis=0):
    return np.max(x, axis=axis) - np.min(x, axis=axis)


def unwrapline(phase):
    # simple-minded phase unwrap algorithm
    for i in range(1,len(phase)):
        diff=phase[i]-phase[i-1]
        if abs(diff)>np.pi:  # need to unwrap
            steps=0
            phaseStep=-np.sign(diff)*2*np.pi
            while abs(diff)>np.pi:
                diff += phaseStep
                steps +=1
                if steps>100:
                    raise "FAILED: unwrapping:"+str(diff-steps*phaseStep)
            phase[i:]+=phaseStep # unwrap for rest of segment
    return phase # necessary if you've sliced


def unwrap2d(ip, amp, minAmp = 1e-1):
    minAmp = max(np.ravel(amp))*minAmp
    unwrapdphase=ip.copy()
    for i in range(unwrapdphase.shape[0]):
        segments=[]
        inSeg=None
        for j in range(unwrapdphase.shape[1]):
            if not inSeg and amp[i,j]>minAmp: # start of segment
                inSeg=1
                segStart=j
            if inSeg and amp[i,j]<minAmp: # end of segment
                inSeg=None
                segments.append( [segStart, j-1] )
        if inSeg: # reached end of line, so end of segment
            segments.append( [segStart,j] )
        if len(segments):
            for segment in segments:
                previousPixel=None
                # search for previous pixel to check for unwrapping in the vertical
                # direction
                for j in range(segment[0],segment[1]+1):
                    if amp[i-1,j]>minAmp:
                        previousPixel=j
                        break
                if previousPixel:
                    # vertical unwrapdphase unwrap algorithm
                    vertDiff=(unwrapdphase[i,previousPixel]
                              -unwrapdphase[i-1,previousPixel])
                    if abs(vertDiff)>np.pi: # need to unwrap
                        steps=0
                        phaseStep=-np.sign(vertDiff)*2*np.pi
                        while abs(vertDiff)>=np.pi:
                            vertDiff+=phaseStep
                            steps+=1
                            if steps>100:
                                raise "FAILED: vertical unwrapping:"+str(i)+"/"+str(j) \
                                      +"/"+str(vertDiff-steps*phaseStep)
                        unwrapdphase[i,segment[0]:segment[1]]+=phaseStep*steps
                    # unwrap backward and then forward, about this pixel
                    unwrapdphase[i,previousPixel:segment[0]-1:-1] = \
                        unwrapline(unwrapdphase[i,previousPixel:segment[0]-1:-1])
                    unwrapdphase[i,previousPixel:segment[1]+1]    = \
                        unwrapline(unwrapdphase[i,previousPixel:segment[1]+1])
                else:
                    # unwrap whole segment regardless of previous line
                    unwrapline(unwrapdphase[i,segment[0]:segment[1]+1])
        else:
            pass

    return unwrapdphase


def unwrap_ref(low_f, high_f, folder):
    np.Float = np.float32
    fName = folder + '/' + high_f
    phase = np.load(fName)
    newphase = np.zeros([phase.shape[0] + 2, phase.shape[1] + 2], np.Float)
    newphase[1:-1, 1:-1] = phase
    amp = np.where(newphase != 0, 1, 0)
    minAmp = 1e-1
    minAmp *= max(np.ravel(amp))
    print("unwrapping...")
    unwrapdphase = unwrap2d(newphase, amp)
    wr_save = folder + '/unwrap.npy'
    np.save(wr_save, unwrapdphase, allow_pickle=False)
    unwrapdphase *= 1.0
    cv2.imwrite(folder + '/reference.png', unwrapdphase)
    # print('ref range', a_range(reference, 1))
    print("(done)")


if __name__ == "__main__":
    np.Float=np.float32
    fName="scan_wrap2.npy"
    phase = np.load(fName)
    newphase = np.zeros([phase.shape[0]+2, phase.shape[1]+2], np.Float)
    newphase[1:-1, 1:-1]=phase
    amp = np.where(newphase!=0,1,0)
    minAmp = 1e-1
    minAmp *= max(np.ravel(amp))
    print("unwrapping...")
    unwrapdphase = unwrap2d(newphase,amp)
    wr_save = 'minunwrap.npy'
    np.save(wr_save, unwrapdphase, allow_pickle=False)
    print('output shape:', unwrapdphase.shape)
    unwrapdphase *= 30.0
    cv2.imwrite('unwrapped.png', unwrapdphase)
    print("(done)")

    try:
        import pylab
        pylab.subplot(1,2,1)
        pylab.imshow( newphase )
        pylab.title("wrapped")
        pylab.subplot(1,2,2)
        pylab.imshow( unwrapdphase )
        pylab.title("unwrapped")

        print("waiting to show plot")
        pylab.show()
        print("and now ending")
    except:
        print("*** Could not plot ***")
    print("Range of phases:")
    print("\tInput (/pi)\t"+str(float(0.1*int(newphase.ptp()/np.pi*10)))
          + " (should be 2, -pi->+pi)")
    print("\tUnwrapped (/pi)\t"+str(float(0.1*int(unwrapdphase.ptp()/np.pi*10))))
