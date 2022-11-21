import { Url } from '../../common/types';

export interface MeResponse {
  meUrls: {
    shortIntro: Url;
    education: Url;
    workExperience: Url;
    compSci: Url;
    hobbies: Url;
  };
}
