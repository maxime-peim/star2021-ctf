#include <iostream>
#include <string>
#include <fstream>
#include <limits>

//g++ use-after-free.cpp -o use-after-free

struct Matrix;

struct Neo
{
    int hp;
    void (*chooseAPill)(Neo*);
    bool (*protectSion)(Neo*, bool);
    void (*hackTheMatrix)(Matrix*);
    int isAlive;
};

struct Matrix
{
    int hp;
    void (*chaseNeo)(Neo*);
    bool (*attackSion)(bool);
    void (*looseControl)(Matrix*);
    int isOnline;
};

void chaseNeo(Neo *neo) {
    if(neo->isAlive == 0) {
        std::cout << "Neo is already dead." << std::endl;
    }
    else if(neo->isAlive == 1) {
        std::cout << "Agent Smith kills Neo." << std::endl;
        neo->isAlive = 0;
        delete neo;
    }
    else {
        std::cout << "Neo has awaken, Agent Smith is not powerful enough to kill him." << std::endl;
    }
}

bool attackSion(bool underAttack){
    if(underAttack) {
        std::cout << "Sion is already under attack." << std::endl;
    }
    else {
        std::cout << "The Matrix launches an attack against Sion." << std::endl;
    }
    return true;
}

void looseControl(Matrix* matrix){
    std::cout << "The Matrix loose control over Agent Smith who ends up destroying the Matrix." << std::endl;
    matrix->isOnline = 0;
    delete matrix;
}

void chooseAPill(Neo* neo) {
    std::cout << "Which pill do you choose ?" << std::endl;
    std::cout << "1/ Blue\n2/ Red" << std::endl;
    int choice{};
    switch(choice) {
        case 1:
            std::cout << "Ignorance is the right choice sometimes..." << std::endl;
            break;
        case 2:
            std::cout << "So you choose the hard path... Good luck." << std::endl;
            neo->isAlive = 2;
            break;
    }
}

bool protectSion(Neo *neo, bool underAttack) {
    if(underAttack) {
        if(neo->isAlive == 1) {
            std::cout << "Neo hasn't awaken and cannot protect Sion." << std::endl;
            return true;
        }
        else if (neo->isAlive == 0) {
            std::cout << "Neo is dead and cannot protect Sion." << std::endl;
            return true;
        }
        else {
            std::cout << "Neo protects Sion against the attack." << std::endl;
            return false;
        }
    }
    else {
        std::cout << "Sion is not under attack." << std::endl;
        return false;
    }
}

void hackTheMatrix(Matrix* matrix) {
    std::cout << "Neo hacks the Matrix and destroys it!" << std::endl;
    matrix->isOnline = 0;
    std::cout << "Congrats ! Here's your reward:" << std::endl;
    std::ifstream file{"flag.txt"}; 
    if(!file) {
        std::cout << "Error while opening the file. Please contact an admin." << std::endl;
        return;
    }
    std::string flag{};
    std::getline(file, flag);
    std::cout << flag << std::endl;
}

void secured_entry(int &var) {
    while (!(std::cin >> var)) {
        if (std::cin.eof()) {
            throw std::runtime_error("Error while reading your choice");
        }
        else if (std::cin.fail()) {
            std::cout << "Invalid entry. Try again." << std::endl;
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
    }
}

int main() {
    Neo *neo = nullptr;
    Matrix *matrix = nullptr;
    bool sionUnderAttack = false;
    bool end = false;
    while(!end) {
        std::cout << "Loading Architect 2.0..." << std::endl;
        std::cout << "You're the Architect of the Matrix." << std::endl;
        std::cout << "Who do you want to control ?\n1/ The Matrix\n2/ Neo\n3/ Quit" << std::endl;
        int choice{};
        secured_entry(choice);
        switch(choice) {
            case 1:
                std::cout << "What do you want to do with the Matrix ?" << std::endl;
                std::cout << "0/ Create a Matrix\n1/ Chase Neo\n2/ Attack Sion\n3/ Launch all forces against Neo" << std::endl;
                secured_entry(choice);
                switch(choice) {
                    case 0:
                        if(matrix  == nullptr) {
                            matrix = new Matrix;
                            matrix->attackSion = attackSion;
                            matrix->chaseNeo = chaseNeo;
                            matrix->hp = 5000;
                            matrix->isOnline = 1;
                            matrix->looseControl = looseControl;
                        }
                        else {
                            std::cout << "The matrix is already online." << std::endl;
                        }
                        break;
                    case 1:
                        if(matrix->isOnline) {
                            matrix->chaseNeo(neo);
                        }
                        else {
                            std::cout << "The Matrix is not online." << std::endl;
                        }
                        break;
                    case 2:
                        if(matrix->isOnline) {
                            sionUnderAttack = matrix->attackSion(sionUnderAttack);
                        }
                        else {
                            std::cout << "The Matrix is not online." << std::endl;
                        }
                        break;
                    case 3:
                        if(matrix->isOnline)
                        {
                            matrix->looseControl(matrix);
                        }
                        else {
                            std::cout << "The Matrix is not online." << std::endl;
                        }
                        break;
                    default:
                        std::cout << "Could not understand your choice" << std::endl;
                        break;
                }
                break;
            case 2:
                std::cout << "What do you want to do with Neo?" << std::endl;
                std::cout << "0/ Create a new Neo\n1/ Choose a pill\n2/ Protect Sion\n3/ Hack The Matrix" << std::endl;
                secured_entry(choice);
                switch(choice) {
                    case 0:
                    if(neo == nullptr) {
                        neo = new Neo;
                        neo->chooseAPill = chooseAPill;
                        neo->hackTheMatrix = hackTheMatrix;
                        neo->hp = 100;
                        neo->isAlive = 1;
                        neo->protectSion = protectSion;
                    }
                    else {
                        std::cout << "Neo is already alive." << std::endl;
                    }
                    break;
                    case 1:
                        if(neo->isAlive) {
                            neo->chooseAPill(neo);
                        }
                        else {
                            std::cout << "Neo is dead." << std::endl;
                        }
                        break;
                    case 2:
                        if(neo->isAlive) {
                            neo->protectSion(neo, sionUnderAttack);
                        }
                        else {
                            std::cout << "Neo is dead." << std::endl;
                        }
                        break;
                    case 3:
                        if(neo->isAlive) {
                            std::cout << "Neo is not powerful to hack the Matrix and dies trying." << std::endl;
                            neo->isAlive = 0;
                            delete neo;
                        }
                        else {
                            std::cout << "Neo is dead." << std::endl;
                        }
                        break;
                    default:
                        std::cout << "Could not understand your choice" << std::endl;
                        break;
                }
                break;
            case 3:
                std::cout << "Quitting..." << std::endl;
                end = true;
                break;
            default:
                std::cout << "Could not understand your choice" << std::endl;
                break;
        }
    }
    return 0;
}