import re

class ET:
    '''ET can, equipt with an emotion, modifier and reduction list, analyze sentences for emotion terms '''
    def __init__(self, emotion_dict: dict, intensifiers: list, negations: list, answer_columns: list = None, first_ignore: bool = True) -> None:
        self.emotion_dict = emotion_dict
        self.intensifiers = intensifiers
        self.negations = negations
        self.answer_columns = answer_columns
        self.first_ignore = first_ignore


    def check_df(self, df: list, answer_columns: list = None) -> list:

        if answer_columns is None:
            answer_columns = self.answer_columns


        # 0 = Verständnisfrage
        # 1 = no Reduction
        # 2 = over 2
        # 3 = 0
        problems = {}
        check = []
        for i,line in enumerate(df):

            if line.matches is not None:
                continue

            counter = 0
            out = []

            for key, col in line.anwers.items():
                out.append({key:self.check_line(col)})

            for y in out:
                counter += len(y)

            if counter == 1:            
                if self.first_ignore:
                    if out[0] != []:
                        problems[i] = [out, 0]
                        continue
                
                for i in out:
                    if i != []:
                        df['Emotion'][ind] = i[0].emotion
                        df['Reduction'][ind] = i[0].reduction
                        df['Modifikator'][ind] = i[0].modifier
                        df['Negation'][ind]  = i[0].negation
                        df['Kodierer'][ind]  = "E.T."
                        df['Problem'][ind]  = ""
                if df['Reduction'][ind] == "":
                    problems[ind] = [out, 1]
            
            elif counter > 1:
                emos = []
                for z in range(len(out)):
                    for i in out[z]:
                        if i != []:
                            emos.append(i.emotion)
                            #for y in out:
                            #    if y != []:
                            #        if i.emotion != y.emotion:
                            #            sameEmo = False
                            
                if len(Counter(emos).values()) == 1:
                    for i in out:
                        if i != []:
                            df['Emotion'][ind] = i[0].emotion
                            df['Reduction'][ind] = i[0].reduction
                            df['Modifikator'][ind] = i[0].modifier
                            df['Negation'][ind]  = i[0].negation
                            df['Kodierer'][ind]  = "E.T."
                            df['Problem'][ind]  = ""
                else:
                    problems[ind] = [out, 2]
            else:
                problems[ind] = [out, 3]

            check.append(counter)

        for ind in problems:
            df['Problem'][ind] = problems[ind][1]

        

        return problems, df


    def check_line(self, line: list) -> list:
        '''This function is the main method of ET
        if presented with a sentence in string format, it analyzes it for used emotions and its connected intensifiers and negations'''
        
        if not line:
            return [[[],[],[]]]

        out = []

        while len(line) > 0:

            matches = []

            for emotion in self.emotion_dict.keys():
                try:
                    if [x.lower() for x in line[-len(emotion):len(line)]] == [x.lower() for x in list(emotion)]:
                        matches.append(emotion)
                except IndexError:
                    continue
                
            if not matches:
                line = line[:-1]
                continue
            
            found_emotion = max(matches, key=len)

            line = line[:-len(found_emotion)]
            
            matches_tmp = []

            while len(line)>0:

                matches = []

                for intensifier in self.intensifiers:
                    try:
                        if [x.lower() for x in line[-len(intensifier):len(line)]] == [x.lower() for x in intensifier]:
                            matches.append(intensifier)
                    except IndexError:
                        continue

                if not matches:
                    break
                
                match_tmp = max(matches, key=len)
                line = line[:-len(match_tmp)]
                matches_tmp.insert(0,match_tmp)

            found_intensifier = matches_tmp

            matches_tmp = []

            while len(line)>0:

                matches = []

                for negation in self.negations:
                    try:
                        if [x.lower() for x in line[-len(negation):len(line)]] == [x.lower() for x in negation]:
                            matches.append(negation)
                    except IndexError:
                        continue

                if not matches:
                    break
                
                match_tmp = max(matches, key=len)
                line = line[:-len(match_tmp)]
                matches_tmp.insert(0,match_tmp)

            found_negation = matches_tmp

            out.append([found_emotion,found_intensifier,found_negation])
        
        return out