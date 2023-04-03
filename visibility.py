# Author: Máximo Rodríguez Herrero
# maximo.rodriguez@estudiante.uam.es
# Universidad Autónoma de Madrid

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import astropy.units as u

from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun, get_moon, Angle
from astropy.visualization import astropy_mpl_style, quantity_support
from astroplan.plots import plot_sky
from astroplan import Observer

class ObjectVisibility():
    """Class used to provide insights about the object visibiliy, air-mass calculation, path
    through the night sky etc
    Use: 
        Define the location of your observatory using EarthLocation from astropy.coordinates ex:
        calar_alto = EarthLocation(lat = 37.2236*u.deg, lon = -2.5461*u.deg, height = 2168*u.m)
        
        Then, define the object, date, UTC offset of the observation, ex:
        utcoffset = 1*u.hour  
        NGC5395 = ObjectVisibility('2020-3-10', utcoffset, calar_alto, 'NGC5395')
        
        The class admits working with the name of the object (if present in Astropy's database or, 
        if not, with right ascension, declination coordinates"""
    def __init__(self, civil_date, utc_off, earth_loc, ob_name, ar=0, dec=0):
        """
        - inputs:
            - civil_date = 'yy-mm-dd'
            - utc_off = utc offset
            - earth_loc = astroy frame of the observation place
            - ob_name = 'name'
            - ar, dec = coordinates of the object
        """
        # visualize astropy quantities
        quantity_support()
        # coordinates of the object by name or by right ascension, declination coordinates
        self.ob_name = ob_name
        # if the coordinates are not give search by name in the astropy survay:
        if ar == 0:
            self.object = SkyCoord.from_name(ob_name)
        else:
            self.object = SkyCoord(ra = ar, dec = dec)
        # time utc offset
        self.utc_off = utc_off
        # observatory location on earth
        self.earth_loc = earth_loc
        # midnight time in the observatory UTC
        self.midnight = Time(civil_date +' 00:00:00') - utc_off
        # observation time from today's 12 to tomorrow's 12 
        self.delta_midnight = np.linspace(-12, 12, 1000)*u.hour
        self.times_ObsDay = self.midnight + self.delta_midnight
        # reference frame of observation
        self.frame_ObsDay = AltAz(obstime = self.times_ObsDay, location = self.earth_loc)
        # sun position in the observation reference frame
        self.sun_ObsDay = get_sun(self.times_ObsDay).transform_to(self.frame_ObsDay)
        # moon position in the observation reference frame
        self.moon_ObsDay = get_moon(self.times_ObsDay).transform_to(self.frame_ObsDay)
        # object position in the observation reference frame
        self.object_ObsDay = self.object.transform_to(self.frame_ObsDay)
        # index slicing: TRUE if the sun is hidden and the object above 30º
        self.index = self.visible_index()
        if np.sum(self.index) != 0:
            # total observation hours
            self.visible_hours = np.round(self.delta_midnight[self.index][-1] - self.delta_midnight[self.index][0], 2)
    def visible_index(self, alpha=30):
        """index such that the sun is bellow horizon and the object above alpha degrees
        - inputs: 
            - alpha: minimum observable altitude in degrees of the observatory"""
        index = (self.sun_ObsDay.alt < 0*u.deg)*(self.object_ObsDay.alt > alpha*u.deg)
        if sum(index) == 0:
            print('NO SE PUEDE OBSERVAR ESTE OBJETO ' + self.ob_name)
            return 0
        else:
            return index 
    
    def plot_alt(self, axis=0, save=False, figsize=(8,5)):
        """plot the altitude of the sun, moon and astronomical object together with the 
        night time and the lines such that the object is above 30º
        - input:
            - axis: axis to place the figure in
            - save: True to save the figure in IMAGES/object_name.png
            - figsize: figure size parameters"""
        plt.style.use(['science', 'notebook', 'grid'])
        if axis == 0:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            ax = axis
        # altitudes moon, sun and object
        ax.plot(self.delta_midnight, self.sun_ObsDay.alt, 'r-', label = 'Sun')
        ax.plot(self.delta_midnight, self.moon_ObsDay.alt, color = [0.45]*3, ls = '-', label = 'Moon')
        ax.plot(self.delta_midnight, self.object_ObsDay.alt, 'b-', label = self.ob_name)
        # shaded areas, evening and closed night
        ax.fill_between(self.delta_midnight, 0*u.deg, 90*u.deg, self.sun_ObsDay.alt < -0*u.deg, color = '0.5', zorder = 0)
        ax.fill_between(self.delta_midnight, 0*u.deg, 90*u.deg, self.sun_ObsDay.alt < -18*u.deg, color = '0.2', zorder = 0)
        # vertical lines delimiting the observation time (above 30º)
        if np.sum(self.index) != 0:
            ax.axvline(x = self.delta_midnight[self.index][0], color = 'y')
            ax.axvline(x = self.delta_midnight[self.index][-1], color = 'y')
        # limit x axis
        ax.set_xlim(-12*u.hour, 12*u.hour)
        # time representation as seen in a clock 
        ax.set_xticks((np.arange(13)*2-12)*u.hour)
        ax.set_xticklabels([*[str(i) for i in range(12, 24, 2)], *[str(i) for i in range(0, 13, 2)]])
        ax.set_ylim(0*u.deg, 90*u.deg)
        ax.set_xlabel('Civil Time')
        ax.set_ylabel('Altitude [deg]')
        ax.legend()
        ax.set_title('ra = {:.2f}, dec = {:.2f}'.format(self.object.ra, self.object.dec))
        #plt.show()
        if save:
            fig.savefig('IMAGES/' + self.ob_name + '.png', dpi = 150)
        
    def plot_airmass(self, axis = 0):
        """airmass plot, secant of the altitude of the object
        - input:
            - axis: axis to place the figure in"""
        plt.style.use(['science', 'notebook', 'grid'])
        if axis == 0:
            fig, ax = plt.subplots(figsize = (15, 10))
        else:
            ax = axis
        # airmass
        self.airmass = self.object_ObsDay.secz
        # airmass vs time
        ax.plot(self.delta_midnight, self.airmass, 'k-')
        # effective airmass ( object above 30º and sun below 0º)
        if np.sum(self.index) != 0:
            ax.plot(self.delta_midnight[self.index], self.airmass[self.index], 'r-', 
                    label = 'Visible period {}'.format(self.visible_hours))
            ax.plot(self.delta_midnight[self.index][-1], self.airmass[self.index][-1], 'ro', markersize = 10)
            ax.set_title(r'$t_{min}$'+' = {:.1f} airmass = {:.2f}'.format(self.delta_midnight[self.index][-1], 
                                                                          self.airmass[self.index][-1]))
            ax.legend()
        # xlim starts when the sun hides below the horizon empiece en cuanto el sol se oculta por el horizonte
        aux = self.delta_midnight[1:][self.sun_ObsDay.alt[-1:]*self.sun_ObsDay.alt[1:] < 0][0]
        ax.set_xlim(aux, 12*u.hour)
        ax.set_ylim(0, 4)
        ax.set_xlabel('Hours to midnight (UTC {:.0f})'.format(self.utc_off))
        ax.set_ylabel('Airmass [Sec(z)]')
        
        #plt.show()

    def sky_view(self):
        """path of the object in the nigh sky plot"""
        plt.style.use(['science', 'notebook', 'grid'])
        plt.figure(figsize = (8, 5))
        plot_sky(self.object_ObsDay, Observer(location = self.earth_loc, name = 'obs'), self.midnight + self.delta_midnight, 
                 style_kwargs = dict(color = 'k',label = self.ob_name))
        plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
        plt.show()
    def plots(self):
        """plot every figure"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (20, 10))
        self.plot_alt(ax1)
        self.plot_airmass(ax2)
        self.sky_view()