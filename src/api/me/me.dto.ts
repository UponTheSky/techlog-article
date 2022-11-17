import { Url } from '../../common/types';

export interface MeResponse {
  meInfos: {
    profile: Url;
    shortIntro: string;
    education: string;
    workExperience: string;
    compSci: string;
    hobbies: string;
  };
}

export type StaticFileList = (keyof MeResponse['meInfos'])[];
export const staticFileList = [
  'profile',
  'shortIntro',
  'education',
  'workExperience',
  'compSci',
  'hobbies',
  'externalLinks',
] as StaticFileList;
