import re
import pickle
import numpy as np
import pandas as pd
import chemdataextractor as cde
import pubchempy as pcp

import sympy
import itertools
import operator

from chempy import balance_stoichiometry
from chempy import Substance
from chempy import Reaction
from chempy.util import periodic

STOICH_DF = pickle.load(open('./data/processed/stoich_df.p', 'rb'))
THERMO_DF = pickle.load(open('./data/processed/thermo_df.p', 'rb'))


def check_coefficients(reactants, products):
    '''
    Checks whether a possible reactant/product combination would result in a
    valid balanced chemical equation.
    
    --Parameters--
    reactants:      iterable (str)
    products:       iterable (str)
        any iterable containing strings with valid chemical formulas
    
    --Output--
    bool
        
    --Examples--
    >>> check_coefficients(['CH4', 'H2O'], ['CO', 'H2'])
    True
    
    >>> check_coefficients(['CH4', 'H2O'], ['CO2', 'H2O2'])
    False
    
    >>> check_coefficients(['CH4', 'H2O'], ['NaOH'])
    False
    '''
    try:
        balance = balance_stoichiometry(reactants, products)
        # list all the coefficients out
        reac_coef = list(balance[0].values()) + list(balance[1].values())
        # rounds to zero if any of the coefficients are less than 1
        is_positive = np.floor((np.array(reac_coef) >= 1).mean()).astype(bool)
        # rounds to zero if any of the coefficients are sympy relational class
        is_definite = np.floor(
            np.array([isinstance(i, sympy.numbers.Number) for i in reac_coef])
            .mean()).astype(bool)
        return is_positive and is_definite
    except:
        return False


def Z_unique(substances):
    '''
    Returns a set representing unique atomic numbers present within a list of
    chemical formulas.
    
    --Parameters--
    substances:     iterable (str)
        any iterable containing strings with valid chemical formulas
    
    --Output--
    set (int)
        atomic numbers of each unique element present in substances
        
    --Example--
    >>> Z_unique(['CH4', 'H2O'])
    {1, 6, 8}
    '''
    if type(substances) == str:
        substances = [substances]
    composition = []
    for s in substances:
        sub = Substance.from_formula(s)
        composition += [*sub.composition]
    return set(composition)


def formula_state_separator(formula, keep_state=False):
    '''
    Separates the state from a formula string.
    
    --Parameters--
    formula:        str
        a string of a single chemical formula
    
    --Output--
    tuple (str)
        
    --Examples--
    >>> formula_state_separator('NaCl(aq)')
    ('NaCl', 'aq')
    
    >>> formula_state_separator('NaCl')
    'NaCl'
    '''
    try:
        regex = re.search('(?<=\()[aglsq]+', formula)
        formula = formula[:regex.start() - 1]
        if keep_state:
            state = regex.group(0)
            return formula, state
        else:
            return formula
    except:
        return formula


def get_gibbs(formula, energy='G', df=False):
    '''
    Retrieves the free energy value, in J, of a single substance
    
    --Parameters--
    formula:        str
        a string of a single chemical formula
    
    --Output--
    list (float)    
        
    --Examples--
    >>> get_gibbs('NaCl(aq)')
    array([-388735.44])
    '''
    if (THERMO_DF['formula'] == formula).max():
        matches = THERMO_DF[THERMO_DF['formula'] == formula]
    else:
        matches = THERMO_DF[THERMO_DF['formula'].map(
            lambda x: x[:len(formula)] == formula)]
        matches = matches[matches['formula'].map(
            formula_state_separator) == formula]

    if df:
        return matches
    else:
        return list(matches[energy])[0]


def state_predictor(formula):
    '''
    Predicts the state of the substance under standard conditions

    --Parameters--
    formula:        str
        a string of a single chemical formula

    --Output--
    str

    --Examples--
    >>> state_predictor('CO2(aq)')
    CO2(g)

    >>> state_predictor('CO2')
    CO2(g)
    '''
    df = get_gibbs(formula, df=True)
    return list(df.sort_values(by='G')['formula'])[0]


def stoich_filter(substances, df=False, thorough=False, exact=False):
    '''
    Returns a masked copy of the stoich dataframe containing elements that
    only contain the elements present in substances. 
    
    --Parameters--
    substances:     iterable (str)
        any iterable containing strings with valid chemical formulas
    
    --Output--
    DataFrame or list (str)

    --Examples--
    >>> stoich_filter('CO2(g)')
    ['O(g)', 'O3(g)', 'C(s)', 'CO3-2(aq)', 'C(s)', ...]

    >>> stoich_filter('CO2(g)', exact=True)
    ['CO2(aq)', 'CO2(g)']
    '''
    if type(substances) == str:
        substances = [substances]

    stoich_temp = STOICH_DF.copy()

    # mask to keep the charge and formula columns in final dataframe
    z_keep = [0, 'formula'] + list(Z_unique(substances))

    # get all other columns
    column_mask = [col for col in stoich_temp.columns if col not in z_keep]
    for col in column_mask:
        # return the dataframe where these columns are all 0
        stoich_temp = stoich_temp[stoich_temp[col] == 0]

    # keep the columns where it's not all zero
    stoich_temp = stoich_temp.loc[(stoich_temp.drop(
        columns=['formula']) != 0).any(axis=1)]

    if exact:
        thorough = True
        substance = Substance.from_formula(substances[0])
        composition = substance.composition
        for z in list(composition.keys()):
            stoich_temp = stoich_temp[stoich_temp[z] == composition[z]]

    # return the dataframe with the columns we want to keep
    if df:
        return stoich_temp[z_keep]
    else:
        stoich_list = list(stoich_temp['formula'])
        if thorough:
            return [f for f in stoich_list]
        else:
            stoich_list = [formula_state_separator(f) for f in stoich_list]
            substances = [formula_state_separator(s) for s in substances]
            return set([state_predictor(f) for f in stoich_list if f not in substances])


def formula_rearranger(formula):
    '''
    (maybe?) fixes the order of elements listed in a chemical formula.
    
    --Parameters--
    formula:        str
        a string of a single chemical formula
    
    --Output--
    str

    --Examples--
    >>> formula_rearranger('ClNa')
    NaCl

    >>> formula_rearranger('BaO4S')
    BaSO4
    '''
    # https://stackoverflow.com/questions/1518522/
    def most_common(L):
        # get an iterable of (item, iterable) pairs
        SL = sorted((x, i) for i, x in enumerate(L))
        # print 'SL:', SL
        groups = itertools.groupby(SL, key=operator.itemgetter(0))
        # auxiliary function to get "quality" for an item
        def _auxfun(g):
            item, iterable = g
            count = 0
            min_index = len(L)
            for _, where in iterable:
                count += 1
                min_index = min(min_index, where)
            # print 'item %r, count %r, minind %r' % (item, count, min_index)
            return count, -min_index
    # pick the highest-count/earliest item
        return max(groups, key=_auxfun)[0]

    if formula in list(THERMO_DF['formula']):
        return formula
    elif formula in list(THERMO_DF['abbrv']):
        return formula
    elif formula in list(THERMO_DF['formula'].apply(formula_state_separator)):
        return formula
    else:
        formulas = stoich_filter(formula, exact=True)
        formulas = [formula_state_separator(f) for f in formulas]
        return most_common(formulas)


def formula_from_name(name):
    '''
    Requests formula from pubchem from a name.
    
    --Parameters--
    name:       str
        a string of a substance's name
    
    --Output--
    str

    --Examples--
    >>> formula_from_name('titanium (iv) oxide')
    TiO2

    >>> formula_rearranger('titanium dioxide')
    TiO2
    '''
    names = list(THERMO_DF['name'])
    nicknames = list(THERMO_DF['abbrv'])

    target = []
    for n in names:
        try:
            if name in n:
                target.append(n)
        except:
            for nn in nicknames:
                try:
                    if name in nn:
                        target.append
                except:
                    pass

    formulas = pcp.get_compounds(name, 'name', listkey_count=1)
    formula = formulas[0].molecular_formula
    formula = formula_rearranger(formula)
    return formula


def standard_gibbs_free_energy(reactants, products, kJ=True):
    '''
    Returns the overall delG of a reaction under standard conditions. 
    
    --Parameters--
    reactants:      iterable (str)
    products:       iterable (str)
    
    --Output--
    float
        
    --Examples--
    >>> standard_gibbs_free_energy(['Na', 'H2O'], ['NaH', 'O2'])
    340.36
    '''
    products = [state_predictor(p) for p in products]
    reactants = [state_predictor(r) for r in reactants]
    equation = balance_stoichiometry(reactants, products)
    # each side is a formula, coefficient tuple
    prod = list(equation[1].items())
    reac = list(equation[0].items())
    delG = 0
    # s[0] is the formula, with or without state
    # s[1] is the coefficient

    def gibbs_sum(side):
        interim_delG = 0
        for s in side:
            interim_delG += get_gibbs(s[0]) * s[1]
        return interim_delG

    delG = gibbs_sum(prod) - gibbs_sum(reac)
    return delG / (1 + 999*kJ)


def reaction_predictor(reactants, max_length=12):
    '''
    Returns the balanced chemical equation of the predicted reaction based on
    minimizing overall delG values.
    
    --Parameters--
    reactants:      iterable(str)
        any iterable containing strings with valid chemical formulas
    
    --Output--
    chempy.chemistry.Reaction
        
    --Examples--
    >>> reaction_predictor(['Al', 'O2'])
    4 Al + 3 O2 → 2 Al2O3
    '''
    reactants = [state_predictor(r) for r in reactants]
    possibilities = stoich_filter(reactants)
    print('scoping possibilities...')
    if len(possibilities) > max_length:
        possibilities = np.array(list(possibilities))
        energies = np.array(
            [get_gibbs(s, 'G') / get_gibbs(s, 'mass') for s in possibilities])
        indices = energies.argsort()
        sorted_possibilities = possibilities[indices]
        possibilities = sorted_possibilities[:(max_length)]

    print('  optimizing combinations...')
    combinations = []
    print(possibilities)
    comb_length = min(6, len(reactants) + 3)
    for i in range(1, comb_length):
        combinations += list(itertools.combinations(possibilities, i))
    combinations = [c for c in combinations if Z_unique(
        c) == Z_unique(reactants)]
    print(combinations)

    print('    deriving equations...')
    good_combinations = []
    for i, comb in enumerate(combinations):
        if check_coefficients(reactants, comb):
            good_combinations.append(comb)

    print('      calculating energies...')
    energies = []
    for gc in good_combinations:
        energies.append(standard_gibbs_free_energy(reactants, gc))

    best_energy = min(energies)
    best_index = energies.index(best_energy)
    best_reaction = Reaction(*balance_stoichiometry(
        reactants, good_combinations[best_index]))

    print(best_reaction)
    print(f'delG = {best_energy:.4} kJ mol-1')

    return best_reaction
