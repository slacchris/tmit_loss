import epics
import meme
import pandas as pd
import argparse

class TMITLoss:
    def __init__(self):
    
        parser = argparse.ArgumentParser()
        parser.add_argument("bsa")
        args = parser.parse_args()
    
    
        self.beampath = epics.caget(<BEAMPATH_PV>) # <--------------------------
        self.wire = epics.caget(<MY_WIRE_PV>) # <-------------------------------
        self.edef = args.bsa

        if beampath == "SC_DIAG0":
            self.rate = epics.caget("TPG:SYS0:1:DST01:RATE_RBV")
        elif beampath == "SC_BSYD":
            self.rate = epics.caget("TPG:SYS0:1:DST02:RATE_RBV")
        elif beampath == "SC_HXR":
            self.rate = epics.caget("TPG:SYS0:1:DST03:RATE_RBV")
        elif beampath == "SC_SXR":
            self.rate = epics.caget("TPG:SYS0:1:DST04:RATE_RBV")

        replace_wire = self.wire.replace("WIRE", "")
        replace_colon = replace_wire.replace(":", "")
        self.region = replace_colon[0:-3]

        if self.region == "DOG" or "BPN" in self.region:
            self.region = "BYP"

        # PV should contain the region 
        # BPM selections change based on region

        htr = {}
        htr["before"] = ["BPMS:GUNB:925", "BPMS:HTR:120", "BPMS:HTR:320"]
        htr["after"] = ["BPMS:HTR:760", "BPMS:HTR:830", "BPMS:HTR:860", 
	                    "BPMS:HTR:960"]

        col1 = {}
        col1["before"] = ["BPMS:BC1B:125", "BPMS:BC1B:440", "BPMS:COL1:120", 
                          "BPMS:COL1:260", "BPMS:COL1:280", "BPMS:COL1:320"]
        col1["after"] = ["BPMS:BPN27:400", "BPMS:BPN28:200", "BPMS:BPN28:400",
                         "BPMS:SPD:135", "BPMS:SPD:255", "BPMS:SPD:340", 
                         "BPMS:SPD:420", "BPMS:SPD:525"]

        ltus = {}
        ltus["before"] = ["BPMS:BPN27:400", "BPMS:BPN28:200", "BPMS:BPN28:400",
                          "BPMS:SPD:135", "BPMS:SPD:255", "BPMS:SPD:340", 
                          "BPMS:SPS:572", "BPMS:SPS:580", "BPMS:SPS:640", 
                          "BPMS:SPS:710", "BPMS:SPS:770", "BPMS:SPS:780", 
                          "BPMS:SPS:830", "BPMS:SPS:840", "BPMS:SLTS:150"]
        ltus["after"] = ["BPMS:LTUS:660", "BPMS:LTUS:680", "BPMS:LTUS:740", 
                          "BPMS:LTUS:750"]

        emit2 = {}
        emit2["before"] = ["BPMS:BC2B:150", "BPMS:BC2B:530", "BPMS:EMIT2:150", 
                           "BPMS:EMIT2:300" ]
        emit2["after"] = ["BPMS:EMIT2:800", "BPMS:EMIT2:900" "BPMS:L3B:1683"]

        byp = {}
        byp["before"] = ["BPMS:L3B:3583", "BPMS:EXT:351", "BPMS:EXT:748", 
                         "BPMS:DOG:120", "BPMS:DOG:135", "BPMS:DOG:150", 
                         "BPMS:DOG:200", "BPMS:DOG:215", "BPMS:DOG:230",
                         "BPMS:DOG:280", "BPMS:DOG:335", "BPMS:DOG:355",
                         "BPMS:DOG:405"]
        byp["after"] = ["BPMS:BPN23:400", "BPMS:BPN24:400", "BPMS:BPN25:400",
                        "BPMS:BPN26:400", "BPMS:BPN27:400", "BPMS:BPN28:200",
                        "BPMS:BPN28:400", "BPMS:SPD:135", "BPMS:SPD:255",
                        "BPMS:SPD:340", "BPMS:SPD:420", "BPMS:SPD:525",
                        "BPMS:SPD:570", "BPMS:SPD:700", "BPMS:SPD:955"]

        diag0 = {}
        diag0["before"] = ["BPMS:DIAG0:190", "BPMS:DIAG0:210", "BPMS:DIAG0:230",
                           "BPMS:DIAG0:270", "BPMS:DIAG0:285", "BPMS:DIAG0:330",
                           "BPMS:DIAG0:370", "BPMS:DIAG0:390"]
        diag0["after"] = ["BPMS:DIAG0:470", "BPMS:DIAG0:520"]

        self.bpms = {"htr": htr,
                     "col1": col1,
                     "ltus": ltus,
                     "emit2": emit2,
                     "byp": byp,
                     "diag0": diag0,
                     }

        self.waveform = self.calculate_tmit_loss()
        try:
            sectors = ["HTR", "COL1", "EMIT2", "DIAG0", "LTUS", "BYP"]
            for sector in sectors
                my_waveform_pv = f"BSA:{sector}:{self.edef}:TmitLoss"
                epics.caput(<MY_WAVEFORM_PV>, self.waveform) # <------------------------
        except:
            error = "Error writing waveform PV"
            epics.caput(<MY_STATUS_REPORT>, error)

    def get_bpm_list(self):
        try:
            bpm_tmit_pvs = meme.names.list_pvs("BPMS:%:TMIT", 
                tag = self.beampath,
                sort_by = "z")
            self.bpm_tmit_pvs = bpm_tmit_pvs
        except:
            error = "Error getting PV names from Directory Service"
            epics.caput(<MY_STATUS_REPORT>, error)

    def get_bsa_counts(self):
        try:
            counts = epics.caget("BSA:SYS0:1:" + str(self.edef) + ":CNT")
            self.counts = counts
        except:
            error = "Error getting BSA counts"
            epics.caput(<MY_STATUS_REPORT>, error)

    def get_bpm_data(self):
        try:
            tmit_hst_pvs = []
            for pv in self.bpm_tmit_pvs:
                tmit_hst_pv = pv + "HST" + str(self.edef)
                tmit_hst_pvs.append(tmit_hst_pv)

            unclean_tmit_data = epics.caget_many(tmit_hst_pvs)
            clean_tmit_data = list(filter(
                lambda item: item is not None, unclean_tmit_data))

            for i in range(len(clean_tmit_data)):
                clean_tmit_data[i] = clean_tmit_data[i][0:self.counts]

            tmit_dataframe = pd.DataFrame(data = clean_tmit_data)
            clean_tmit_dataframe = tmit_dataframe.dropna(how = "any")
            self.tmit_data = clean_tmit_dataframe
        except:
            error = "Error getting BPM data from buffer"
            epics.caput(<MY_STATUS_REPORT>, error)

    def iron_bpms(self):
        try:
            tmit_median = self.tmit_data.median()
            ironed_tmit = self.tmit_data.divide(tmit_median)
            self.tmit_iron = ironed_tmit
        except:
            error = "Error ironing BPMs"
            epics.caput(<MY_STATUS_REPORT>, error)

    def shift_bpm_data(self, sector):
        try:
            before_indices = [i for i, a in enumerate(self.bpm_tmit_pvs) for b in sector_bpms["before"] if a.startswith(b)]
            shifter = self.tmit_iron.iloc[before_indices]
            shifter_mean = shifter.mean()
            shifted_tmit = self.tmit_iron.divide(shifter_mean)
            self.tmit_ratio_shift = shifted_tmit
        except:
            error = "Error shifting BPMs"
            epics.caput(<MY_STATUS_REPORT>, error)

    def subtract_means(self, sector):
        try:
            sector_bpms = self.bpms[sector]
            before_indices = [i for i, a in enumerate(self.bpm_tmit_pvs) for b in sector_bpms["before"] if a.startswith(b)]
            after_indices = [i for i, a in enumerate(self.bpm_tmit_pvs) for b in sector_bpms["after"] if a.startswith(b)]

            tmit_before = self.tmit_ratio_shift.iloc[before_indices]
            mean_before = tmit_before.mean()

            tmit_after = self.tmit_ratio_shift.iloc[after_indices]
            mean_after = tmit_after.mean()

            tmit_waveform = (mean_before - mean_after) * 100

            return tmit_waveform
        except:
            error = "Error subtracting TMIT means"
            epics.caput(<MY_STATUS_REPORT>, error)

    def calculate_tmit_loss(self):
            self.get_bpm_list()
            self.get_bsa_counts()
            self.get_bpm_data()
            self.iron_bpms()
            tmit_loss_waveforms = {}
            for sector in self.bpms.keys():
                self.shift_bpm_data(sector)
                tmit_loss_waveforms[sector] = self.subtract_means(sector)

            return tmit_loss_waveforms

if __name__ == "__main__":
    tl = TMITLoss()