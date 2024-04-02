import matplotlib.pyplot as plt
import numpy as np
from detecta import detect_peaks, detect_onset

class ex_data():
    def grf(data, cols, time, Heel_Strike1, Toe_Off1, Heel_Strike2, Toe_Off2, axis):
        if axis == 'ap':
            title = 'GROUND REACTION FORCE (AP-AXIS)'
        else:
            title = 'GROUND REACTION FORCE (Vertical)'
        y = {
            'max'          : {},
            'max_frame'    : {},
            'min'          : {},
            'min_frame'    : {},
            'Heel_Strike1' : {},
            'Toe_Off1'     : {},
            'Heel_Strike2' : {},
            'Toe_Off2'      : {},
            }

        fig, ax = plt.subplots()
        for col in cols:
            df = data[col]
            plt.plot(time, np.array(df), color = cols[col][-1], label = cols[col][0])
            
            y['Heel_Strike1'][col] = round(df[Heel_Strike1], 2)
            y['Toe_Off1'][col]     = round(df[Toe_Off1], 2)
            y['Heel_Strike2'][col] = round(df[Heel_Strike2], 2)
            y['Toe_Off2'][col]     = round(df[Toe_Off2], 2)

            y['max'][col]       = round(df.max(), 2)
            y['max_frame'][col] = np.where(df == df.max())[0][0]
            y['min'][col]       = round(df.min(), 2)
            y['min_frame'][col] = np.where(df == df.min())[0][0]

        m = data[cols.keys()].max().max()    

        '''
        plt.ylabel('Force [% BW]')
        plt.xlabel('Time [s]')

        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[Heel_Strike1] ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[Toe_Off1]     ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[Heel_Strike2] ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[Toe_Off2]     ,color='k' ,linestyle = '--' ,alpha=0.5)

        plt.axhline(0,color='k',lw=0.9)
        
        plt.text(time[Heel_Strike1] ,y = m, s='Heel Strike1'    ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[Toe_Off1]     ,y = m, s='Toe Off1'   ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[Heel_Strike2] ,y = m, s='Heel Strike2'          ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[Toe_Off2]     ,y = m, s='Toe Off2' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        
        plt.legend()
        plt.tight_layout()
        plt.title(title)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        # plt.savefig(f"figure/grf_{axis}.png", dpi=300, bbox_inches='tight')
        plt.show()
        '''
        return y

    def one_angle(data, cols, time, k_Heel_Strike1, k_Toe_Off1, k_Heel_Strike2, k_Toe_Off2):
        ang = {
            'max'       : {},
            'max_frame' : {},
            'min'       : {},
            'min_frame' : {},
            'Heel_Strike1' : {},
            'Toe_Off1'     : {},
            'Heel_Strike2' : {},
            'Toe_Off2'      : {},
            }
        
        for col in cols:
            
            df = data[col]
            if 'VELOCITY' in col:
                ylb = 'Angular Velocity [deg/s]'
            else:
                ylb = 'Angle [deg]'
                
            fig, ax = plt.subplots()
            plt.plot(time, np.array(df), color = 'firebrick')

            ang['Heel_Strike1'][col] = round(df[k_Heel_Strike1], 2)
            ang['Toe_Off1'][col]     = round(df[k_Toe_Off1], 2)
            ang['Heel_Strike2'][col] = round(df[k_Heel_Strike2], 2)
            ang['Toe_Off2'][col]     = round(df[k_Toe_Off2], 2)

            ang['max'][col]       = round(df.max(), 2)
            ang['max_frame'][col] = np.where(df == df.max())[0][0]
            ang['min'][col]       = round(df.min(), 2)
            ang['min_frame'][col] = np.where(df == df.min())[0][0]
                        
            m = df.max()
            
            '''
            plt.ylabel(ylb)
            plt.xlabel('Time [s]')
            plt.autoscale(axis='x', tight=True)
            plt.axvline(time[Heel_Strike1] ,color='k' ,linestyle = '--' ,alpha=0.5)
            plt.axvline(time[Toe_Off1]     ,color='k' ,linestyle = '--' ,alpha=0.5)
            plt.axvline(time[Heel_Strike2] ,color='k' ,linestyle = '--' ,alpha=0.5)
            plt.axvline(time[Toe_Off2]     ,color='k' ,linestyle = '--' ,alpha=0.5)

            plt.axhline(0,color='k',lw=0.9)
        
            plt.text(time[k_Heel_Strike1] ,y = m, s='Heel Strike1'    ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            plt.text(time[k_Toe_Off1]     ,y = m, s='Toe Off1'   ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            plt.text(time[k_Heel_Strike2] ,y = m, s='Heel Strike2'          ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            plt.text(time[k_Toe_Off2]     ,y = m, s='Toe Off2' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            
            plt.tight_layout()
            plt.title(f'{cols[col]}')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(axis='y')
            # plt.savefig(f"figure/{cols[col]}.png", dpi=300, bbox_inches='tight')
            plt.show()
            '''
        return ang
    
    def kinematic_sequence(data, ks_cols, time, k_Heel_Strike1, k_Toe_Off1, k_Heel_Strike2, k_Toe_Off2):
        ks = {
            'peak' : {},
            'time' : {},
            }
        fig, ax = plt.subplots()
        
        for col in ks_cols:
            plt.plot(time, np.array(data[col]), color = ks_cols[col][-1], label=ks_cols[col][0])
            ks['peak'][col] = round(data[col].max(), 2)
            ks['time'][col] = np.where(data[col] == data[col].max())[0][0]
            
            plt.axvline(time[ks['time'][col]], color = ks_cols[col][-1], linestyle ='-', alpha= 0.7)
        ''' 
        plt.ylabel('Angular Velocity [Deg/s]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[Heel_Strike1] ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[Toe_Off1]     ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[Heel_Strike2] ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[Toe_Off2]     ,color='k' ,linestyle = '--' ,alpha=0.5)
        
        plt.axhline(0,color='k',lw=0.9)
        plt.text(time[k_Heel_Strike1] ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='Heel Strike1' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_Toe_Off1]     ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='Toe Off1' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_Heel_Strike2] ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='Heel Strike2',rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_Toe_Off2]     ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='Toe Off2' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
       
        plt.legend()
        plt.tight_layout()
        plt.title('KINEMATIC SEQUENCE')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        # plt.savefig(f"figure/kinematic.png", dpi=300, bbox_inches='tight')
        plt.show()
        '''
        return ks