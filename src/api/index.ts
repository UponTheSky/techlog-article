import { MainController } from './main/main.controller';
import { MeController } from './me/me.controller';

const mainController = new MainController();
const meController = new MeController();

export const controllers = [mainController, meController];
