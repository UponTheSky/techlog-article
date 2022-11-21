import { Url } from '../../common/types';

export interface MeResponse {
  meUrls: {
    profile: Url;
    shortIntro: Url;
    education: Url;
    workExperience: Url;
    compSci: Url;
    hobbies: Url;
  };
}

export type StaticFileList = (keyof MeResponse['meUrls'])[];
export const staticFileList = [
  'profile',
  'shortIntro',
  'education',
  'workExperience',
  'compSci',
  'hobbies',
  'externalLinks',
] as StaticFileList;
