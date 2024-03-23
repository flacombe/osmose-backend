#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe - 2024                                    ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_power_pole_FR_comac (Analyser_Merge_Point):
    def __init__(self, config, source_url, dataset_name, source, srid, conflationDistance, classs, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8490, id = classs + 1, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole not integrated'))
        self.def_class_possible_merge(item = 8491, id = classs + 3, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:picture'],
            title = T_('Power pole integration suggestion'))
        self.def_class_update_official(item = 8492, id = classs + 4, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole update'))

        self.init(
            source_url,
            dataset_name,
            CSV(source, srid = srid),
            Load_XY('X', 'Y'),
            Conflate(
                select = Select(
                    types = ['nodes'],
                    tags = {'power': 'pole'}),
                osmRef = 'ref',
                conflationDistance = conflationDistance,
                mapping = Mapping(
                    static1 = {'power': 'pole'},
                    static2 = {'source': self.source},
                    mapping1 = {
                        'material': lambda res: self.extract_material.get(res['type_potea']),
                        'height': lambda res: res['hauteur_ho'],
                        'start_date': lambda res: res['annee']},
                text = lambda tags, fields: {} )))

    extract_material = {
        'BOIS': 'wood',
        'BETON': 'concrete',
        'METAL': 'steel'
    }
